#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Wellcome Sanger Institute
import tempfile
import boto3
import uuid
import pypika as ppk
import psycopg2
import psycopg2.extras
import spatialdata
from spatialdata_io import xenium, xenium_aligned_image
import shapely
import h5py
import numpy as np
import hashlib
import fire


def register_features(
    sdata:spatialdata.SpatialData,
    HARMONISED_DATASET_ID:str,
    SEGMENTATION_FLAVOR_ID:str,
    FEATURE_FLAVOR_ID:str,
    y_scale_factor:float,
    x_scale_factor:float,
    bucket:boto3.Bucket,
    s3_uri_prefix:str,
    PATCH_SIZE:int=256,
    host:str='localhost',
    db_user:str='postgres',
    db_password:str='example',
    port:int=5555,
):
    conn = psycopg2.connect(
        dbname='cytoweave_db',
        user=db_user,
        host=host,
        password=db_password,
        port=port
    )
    conn.autocommit = True

    harmonised_datasets = ppk.Table(name="harmonised_datasets", schema="cw_feature_registry")
    # spatialdata_files = ppk.Table(name="spatialdata_files", schema="cw_object_storage")
    segmentations = ppk.Table(name="segmentations", schema="cw_feature_registry")
    segmentation_flavors = ppk.Table(name="segmentation_flavors", schema="cw_feature_metadata")
    features = ppk.Table(name="features", schema="cw_feature_registry")
    array_files = ppk.Table(name="array_files", schema="cw_object_storage")

    # make a database query to find the segmentations

    query = (ppk.PostgreSQLQuery
            .from_(harmonised_datasets)
            .left_join(segmentations)
            .on(harmonised_datasets.id == segmentations.harmonised_dataset_id)
            .left_join(segmentation_flavors)
            .on(segmentations.flavor_id == segmentation_flavors.id)
            .select(segmentations.id, segmentations.segmentation_polygon)
            .where(harmonised_datasets.id == HARMONISED_DATASET_ID)
            .where(segmentation_flavors.id == SEGMENTATION_FLAVOR_ID))
    sql = query.get_sql()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        curs.execute(sql)
        pg_rows = curs.fetchall()

    segmentations_list = pg_rows

    # generate features with uuids for each segmentation

    for segmentation in segmentations_list:
        seg_id, seg_polygon = segmentation

        # generate the features with uuids
        feat_id = uuid.uuid4()
        feat_file_id = uuid.uuid4()

        # generate a query area for extracting the patch

        seg_polygon_parsed = shapely.Polygon(eval(seg_polygon))
        x, y = seg_polygon_parsed.centroid.coords[0]

        patch_box = shapely.box(
            xmin=x - ((PATCH_SIZE * x_scale_factor) / 2),
            xmax=x + ((PATCH_SIZE * x_scale_factor) / 2),
            ymin=y - ((PATCH_SIZE * y_scale_factor) / 2),
            ymax=y + ((PATCH_SIZE * y_scale_factor) / 2)
        )

        # make a spatial query against the spatialdata object

        image_feature_xarray = spatialdata.polygon_query(sdata["histology"], patch_box, target_coordinate_system="global")

        # write the array to a hdf5 store and upload to s3

        s3_path = f"features/{feat_file_id}.h5"

        with tempfile.NamedTemporaryFile() as tmp_file:
        
            with h5py.File(tmp_file.name, 'w') as hdf5_file:
                hdf5_file.create_dataset(str(feat_id), data=np.array(image_feature_xarray))
            
            checksum = hashlib.md5(open(tmp_file.name,'rb').read()).hexdigest()
            
            bucket.upload_file(tmp_file.name, s3_path)
        
        # insert a new record for the hdf5 file
        
        query = (ppk.PostgreSQLQuery
            .into(array_files)
            .insert(feat_file_id, f"{s3_uri_prefix}/{s3_path}", checksum, list(image_feature_xarray.shape), str(image_feature_xarray.dtype), ["c", "x", "y"]))
        sql = query.get_sql()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            curs.execute(sql)

        # insert a new record for the feature

        query = (ppk.PostgreSQLQuery
                .into(features)
                .insert(feat_id, feat_file_id, seg_id, FEATURE_FLAVOR_ID))
        sql = query.get_sql()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            curs.execute(sql)


def main(xenium_sdata_objs:str=[
        "Xenium_Prime_Human_Skin_FFPE_outs",
        "Xenium_Prime_Human_Prostate_FFPE_outs"
    ]):
    FEATURE_FLAVOR_ID = "6f15f4f8-d476-4845-b2e5-f7f1b9b92d65"  # image patch
    HARMONISED_DATASET_ID = "8e32f1b2-9c6f-40d1-90d1-fa2bd3ba0846"
    SEGMENTATION_FLAVOR_ID = "6ce1cb98-be64-4af1-96d2-f3a4b05ac1aa"  # cells

    PATCH_SIZE = 256


    s3_uri_prefix = f"s3://cytoweave/"

    # Configure s3. Should upload separately later.
    s3 = boto3.resource('s3', 
        endpoint_url='http://localhost:9000',
        aws_access_key_id='minioadmin',
        aws_secret_access_key='minioadmin',
        aws_session_token=None,
        config=boto3.session.Config(signature_version='s3v4'),
        verify=False
    )

    bucket = s3.Bucket('cytoweave')

    for xenium_sdata_obj in xenium_sdata_objs:
        sdata = spatialdata.read_zarr(xenium_sdata_obj)
        y_scale_factor = (sdata.images["histology"].y[-1] - sdata.images["histology"].y[0]) / (len(sdata.images["histology"].y) - 1)
        x_scale_factor = (sdata.images["histology"].x[-1] - sdata.images["histology"].x[0]) / (len(sdata.images["histology"].x) - 1)
        register_features(
            sdata, HARMONISED_DATASET_ID, SEGMENTATION_FLAVOR_ID, FEATURE_FLAVOR_ID, PATCH_SIZE,
            x_scale_factor, y_scale_factor,
            bucket=bucket,
            s3_uri_prefix=s3_uri_prefix)

if __name__ == "__main__":
    fire.fire(main)