from typing import List
import pypika as ppk
import psycopg2.extras
import psycopg2
import uuid
import shapely

from .configure_postgres import configure_postgres_connection


def register_segmentations(
        segmentation_polygons: List[shapely.Polygon],
        harmonised_dataset_id: str,
        segmentation_flavor_id: str
) -> List[str]:

    conn = configure_postgres_connection()
    segmentations = ppk.Table(name="segmentations", schema="cw_feature_registry")

    records = []
    segmentation_ids = []
    for segmentation_polygon in segmentation_polygons:
        segmentation_id = str(uuid.uuid4())
        xx, yy = segmentation_polygon.exterior.coords.xy
        segmentation_polygon_postgres = ', '.join([f"({x}, {y})" for x, y in zip(xx.tolist(), yy.tolist())])
        records.append((segmentation_id, segmentation_polygon_postgres, harmonised_dataset_id, segmentation_flavor_id))
        segmentation_ids.append(segmentation_id)

    query = (
        ppk.PostgreSQLQuery.into(segmentations)
        .insert(*records)
    )
    sql = query.get_sql()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        curs.execute(sql)

    return segmentation_ids
