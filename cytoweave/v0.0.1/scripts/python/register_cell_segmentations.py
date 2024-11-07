#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Wellcome Sanger Institute
from spatialdata_io import xenium, xenium_aligned_image
import pypika as ppk
import psycopg2
import psycopg2.extras
import uuid
import fire
import logging
import spatialdata 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register_segmentations(
        xenium_folder:str,
        harmonised_datasets_id:str,
        host:str='172.27.24.164',
        port:int=5555,
        segmentation_flavor_id:str="c3c8a6e2-12e1-4cf8-b7fe-5fd90e182b3c",
        db_user:str='postgres',
        db_password:str='example',
    ):
    conn = psycopg2.connect(
        dbname='cytoweave_db',
        user=db_user,
        host=host,
        password=db_password,
        port=port
    )
    conn.autocommit = True

    sdata = spatialdata.read_zarr(xenium_folder)

    for segmentation_polygon in sdata["cell_boundaries"]["geometry"]:
        xx, yy = segmentation_polygon.exterior.coords.xy
        segmentation_polygon_postgres = ', '.join([f"({x}, {y})" for x, y in zip(xx.tolist(), yy.tolist())])
        segmentation_id = uuid.uuid4()
        segmentations = ppk.Table(name="segmentations", schema="cw_feature_registry")
        query = ppk.PostgreSQLQuery.into(segmentations).insert(
            segmentation_id, segmentation_polygon_postgres, harmonised_datasets_id, segmentation_flavor_id 
        )
        sql = query.get_sql()
        logger.info(sql)
        
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            curs.execute(sql)


def main(xenium_exps:str=[
        ["../Xenium_Prime_Human_Skin_FFPE_outs.zarr", "8e32f1b2-9c6f-40d1-90d1-fa2bd3ba0846"], 
        ["../Xenium_Prime_Human_Prostate_FFPE_outs.zarr", "c14907b9-3364-400e-a86b-71d06221392a"]
    ]):
    for xenium_exp in xenium_exps:
        register_segmentations(xenium_folder=xenium_exp[0], harmonised_datasets_id=xenium_exp[1])


if __name__ == "__main__":
    fire.Fire(main)