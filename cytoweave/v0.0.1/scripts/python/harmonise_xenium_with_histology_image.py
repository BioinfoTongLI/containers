import uuid
import os
import spatialdata
from spatialdata_io import xenium, xenium_aligned_image
import tempfile
from typing import Optional

from .register_and_upload_spatialdata_file import register_and_upload_spatialdata_file
from .register_harmonised_dataset import register_harmonised_dataset

def main(
        xenium_bundle_path: str,
        he_image_path: str,
        he_image_alignment_file_path: str,
        section_id: str,
        harmonised_dataset_id: Optional[str] = None,
        spatialdata_file_id: Optional[str] = None,
) -> str:

    if harmonised_dataset_id is None:
        harmonised_dataset_id = str(uuid.uuid4())

    if spatialdata_file_id is None:
        spatialdata_file_id = str(uuid.uuid4())

    sdata = xenium(
        xenium_bundle_path,
        cells_boundaries=True,
        nucleus_boundaries=False,
        cells_labels=False,
        nucleus_labels=False,
        cells_table=False,
        cells_as_circles=False
    )

    image = xenium_aligned_image(
        he_image_path, 
        he_image_alignment_file_path
    )

    image.data = image.data.rechunk((1, 4096, 4096))
    sdata.images["histology"] = image

    extent = spatialdata.get_extent(sdata)
    bounding_box = [
        (min(extent["x"]), min(extent["y"])),
        (max(extent["x"]), max(extent["y"]))
    ]

    with tempfile.TemporaryDirectory() as tmpdir:

        local_path = os.path.join(tmpdir, f"{harmonised_dataset_id}.zarr")
        sdata.write(local_path)

        register_and_upload_spatialdata_file(
            harmonised_dataset_path=local_path,
            spatialdata_file_id=spatialdata_file_id,
        )

    register_harmonised_dataset(
        section_id=section_id,
        spatialdata_file_id=spatialdata_file_id,
        harmonised_dataset_bounding_box=bounding_box,
        harmonised_dataset_id=harmonised_dataset_id,
    )

    return harmonised_dataset_id
