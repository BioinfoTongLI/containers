import uuid
from typing import Optional
import pypika as ppk
import psycopg2.extras
import psycopg2

from .configure_postgres import configure_postgres_connection


def register_feature(
        segmentation_id: str,
        array_file_id: str,
        feature_flavor_id: str,
        feature_id: Optional[str] = None,
) -> str:

    if feature_id is None:
        feature_id = str(uuid.uuid4())

    conn = configure_postgres_connection()
    features = ppk.Table(name="features", schema="cw_feature_registry")

    print(f"Adding record {feature_id} to cw_feature_registry.features")
    query = (
        ppk.PostgreSQLQuery.into(features)
        .insert(feature_id, array_file_id, segmentation_id, feature_flavor_id)
    )
    sql = query.get_sql()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        curs.execute(sql)

    return feature_id
