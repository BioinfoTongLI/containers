from typing import List, Tuple, Optional
import pypika as ppk
import psycopg2.extras
import psycopg2

from .configure_postgres import configure_postgres_connection


def register_harmonised_dataset(
        section_id: str,
        spatialdata_file_id: str,
        harmonised_dataset_bounding_box: List[Tuple[float, float]],
        harmonised_dataset_id: Optional[str]
) -> str:

    conn = configure_postgres_connection()
    harmonised_datasets = ppk.Table(name="harmonised_datasets", schema="cw_feature_registry")

    polygon_postgres = ', '.join([f"({x}, {y})" for x, y in harmonised_dataset_bounding_box])

    print(f"Adding record {harmonised_dataset_id} to cw_feature_registry.harmonised_datasets")
    query = (
        ppk.PostgreSQLQuery.into(harmonised_datasets)
        .insert(harmonised_dataset_id, polygon_postgres, spatialdata_file_id, section_id)
    )
    sql = query.get_sql()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        curs.execute(sql)

    return harmonised_dataset_id
