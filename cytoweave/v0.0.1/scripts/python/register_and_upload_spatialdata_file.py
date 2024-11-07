import os
import uuid
from typing import Optional
import psycopg2
import psycopg2.extras
import pypika as ppk

from .configure_postgres import configure_postgres_connection
from .configure_s3 import configure_s3_bucket


def register_and_upload_spatialdata_file(
        harmonised_dataset_path: str,
        spatialdata_file_id: Optional[str] = None,
) -> str:

    s3_bucket, s3_bucket_name = configure_s3_bucket()

    conn = configure_postgres_connection()
    spatialdata_files = ppk.Table(name="spatialdata_files", schema="cw_object_storage")

    if spatialdata_file_id is None:
        spatialdata_file_id = str(uuid.uuid4())

    s3_path = f"harmonised_datasets/{str(spatialdata_file_id)}.zarr"
    s3_uri = f"s3://{s3_bucket_name}/{s3_path}"

    print(f"Adding record {spatialdata_file_id} to cw_object_storage.spatialdata_files")
    query = (
        ppk.PostgreSQLQuery.into(spatialdata_files)
        .insert(spatialdata_file_id, s3_uri)
    )
    sql = query.get_sql()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        curs.execute(sql)

    for root, _, files in os.walk(harmonised_dataset_path):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, harmonised_dataset_path)
            remote_path = os.path.join(s3_path, relative_path)
            print(f"Uploading {os.path.join(root, file)} to {remote_path}")
            s3_bucket.upload_file(os.path.join(root, file), remote_path)

    return spatialdata_file_id
