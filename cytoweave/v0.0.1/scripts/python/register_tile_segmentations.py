#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Wellcome Sanger Institute
import pypika as ppk
import psycopg2
import psycopg2.extras
import uuid
import numpy as np
import itertools
import shapely
import spatialdata
import fire
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def register_tile_segmentations(
        xenium_folder:str,
        harmonised_datasets_id:str,
        host:str='172.27.24.164',
        port:int=5555,
        TILE_SIZE:int=100, # in microns
        segmentation_flavor_id:str="6ce1cb98-be64-4af1-96d2-f3a4b05ac1aa",
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

    harmonised_datasets = ppk.Table(name="harmonised_datasets", schema="cw_feature_registry")

    query = ppk.PostgreSQLQuery.from_(harmonised_datasets).select("bounding_box").where(harmonised_datasets.id==harmonised_datasets_id)
    sql = query.get_sql()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        curs.execute(sql)
        pg_rows = curs.fetchall()
        logger.info(pg_rows)

    xmax, ymax, xmin, ymin = [float(x) for x in pg_rows[0][0].replace("(", "").replace(")", "").split(",")]

    # select tiles within the xenium capture area

    sdata = spatialdata.read_zarr(xenium_folder)

    y_scale_factor = (sdata.images["histology"].y[-1] - sdata.images["histology"].y[0]) / (len(sdata.images["histology"].y) - 1)
    x_scale_factor = (sdata.images["histology"].x[-1] - sdata.images["histology"].x[0]) / (len(sdata.images["histology"].x) - 1)

    # Convert the tile size to the scale of the image in pixels
    y_step_size = TILE_SIZE / y_scale_factor
    x_step_size = TILE_SIZE / x_scale_factor

    ys = np.arange(start=ymin, stop=ymax-y_step_size, step=y_step_size)
    xs = np.arange(start=xmin, stop=xmax-x_step_size, step=x_step_size)

    tiles = [shapely.box(x, y, x+TILE_SIZE, y+TILE_SIZE) for x, y in itertools.product(xs, ys)]

    extent = spatialdata.get_extent(sdata["morphology_focus"])
    morphology_focus_bounding_box = shapely.box(
            xmin=extent["x"][0],
            ymin=extent["y"][0],
            xmax=extent["x"][1],
            ymax=extent["y"][1]
    )

    tiles_in_capture_area = [tile for tile in tiles if morphology_focus_bounding_box.contains(tile)]

    for tile in tiles_in_capture_area:
        xx, yy = tile.exterior.coords.xy
        polygon_postgres = ', '.join([f"({x}, {y})" for x, y in zip(xx.tolist(), yy.tolist())])
        segmentation_id = uuid.uuid4()
        segmentations = ppk.Table(name="segmentations", schema="cw_feature_registry")
        query = ppk.PostgreSQLQuery.into(segmentations).insert(
            segmentation_id, polygon_postgres, harmonised_datasets_id, segmentation_flavor_id
        )
        sql = query.get_sql()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            curs.execute(sql)
            

def main(xenium_folders:str=[
            ["../Xenium_Prime_Human_Skin_FFPE_outs.zarr", "8e32f1b2-9c6f-40d1-90d1-fa2bd3ba0846"],
            ["../Xenium_Prime_Human_Prostate_FFPE_outs.zarr", "c14907b9-3364-400e-a86b-71d06221392a"]
        ]
    ):
    for dataset in xenium_folders:
        register_tile_segmentations(
            xenium_folder=dataset[0],
            harmonised_datasets_id=dataset[1],
        )


if __name__ == '__main__':
    fire.Fire(main)