from itertools import islice
from typing import List

from spatialdata_io import xenium

from .register_segmentation import register_segmentations


def main(
        xenium_bundle_path: str,
        harmonised_dataset_id: str,
        segmentation_flavor_id: str,
    ) -> List[str]:

    sdata = xenium(xenium_bundle_path)

    segmentation_ids = []

    def chunk(arr_range, arr_size):
        arr_range = iter(arr_range)
        return iter(lambda: list(islice(arr_range, arr_size)), [])

    batches = list(chunk(sdata["cell_boundaries"]["geometry"], 100))
    total_batches = len(batches)

    for i, segmentation_polygons in enumerate(batches):

        print(f"processing batch {i} of {total_batches} (batch size 100)")

        segmentation_id = register_segmentations(
            segmentation_polygons=segmentation_polygons,
            harmonised_dataset_id=harmonised_dataset_id,
            segmentation_flavor_id=segmentation_flavor_id,
        )

        segmentation_ids.extend(segmentation_id)

    return segmentation_ids
