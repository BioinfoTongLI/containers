from typing import List, Tuple
import psycopg2
import psycopg2.extras
import pypika as ppk
import shapely

from .configure_postgres import configure_postgres_connection


def get_segmentations(
        harmonised_dataset_id: str,
        segmentation_flavor_id: str
) -> List[Tuple[str, shapely.Polygon]]:

    conn = configure_postgres_connection()

    segmentations = ppk.Table(name="segmentations", schema="cw_feature_registry")

    query = (
        ppk.PostgreSQLQuery
        .from_(segmentations)
        .select(segmentations.id, segmentations.segmentation_polygon)
        .where(segmentations.harmonised_dataset_id == harmonised_dataset_id)
        .where(segmentations.flavor_id == segmentation_flavor_id)
    )
    sql = query.get_sql()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        curs.execute(sql)
        pg_rows = curs.fetchall()

    segmentation_result = [(pg_row[0], shapely.Polygon(eval(pg_row[1]))) for pg_row in pg_rows]
    return segmentation_result
