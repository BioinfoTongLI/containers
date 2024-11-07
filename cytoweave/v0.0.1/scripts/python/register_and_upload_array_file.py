import hashlib
import tempfile
import uuid
from typing import Optional, List
import h5py
import numpy as np
import psycopg2
import psycopg2.extras
import pypika as ppk
import xarray

from .configure_postgres import configure_postgres_connection
from .configure_s3 import configure_s3_bucket


def register_and_upload_array_file(
        array: xarray.DataArray,
        array_dimensions: List[str],
        array_file_id: Optional[str] = None,
) -> str:

    s3_bucket, s3_bucket_name = configure_s3_bucket()

    conn = configure_postgres_connection()
    array_files = ppk.Table(name="array_files", schema="cw_object_storage")

    if array_file_id is None:
        array_file_id = str(uuid.uuid4())

    s3_path = f"features/{str(array_file_id)}.h5"
    s3_uri = f"s3://{s3_bucket_name}/{s3_path}"

    with tempfile.NamedTemporaryFile() as tmp_file:

        with h5py.File(tmp_file.name, 'w') as hdf5_file:
            hdf5_file.create_dataset(str(array_file_id), data=np.array(array))

        checksum = hashlib.md5(open(tmp_file.name, 'rb').read()).hexdigest()

        print(f"Uploading {tmp_file.name} to {s3_path}")
        s3_bucket.upload_file(tmp_file.name, s3_path)

    print(f"Adding record {array_file_id} to cw_object_storage.array_files")
    query = (
        ppk.PostgreSQLQuery.into(array_files)
        .insert(array_file_id, s3_uri, checksum, list(array.shape), str(array.dtype), array_dimensions)
    )
    sql = query.get_sql()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        curs.execute(sql)

    return array_file_id
