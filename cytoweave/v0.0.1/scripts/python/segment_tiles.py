from itertools import islice
from typing import List
import numpy as np
import shapely
import spatialdata
from spatialdata_io import xenium
import itertools

from .register_segmentation import register_segmentations


def main(
        xenium_bundle_path: str,
        harmonised_dataset_id: str,
        segmentation_flavor_id: str,
        tile_size: int,
    ) -> List[str]:

    sdata = xenium(xenium_bundle_path)

    extent = spatialdata.get_extent(sdata)

    ys = np.arange(start=min(extent["y"]), stop=max(extent["y"]) - tile_size, step=tile_size)
    xs = np.arange(start=min(extent["x"]), stop=max(extent["x"]) - tile_size, step=tile_size)

    tiles = [shapely.box(x, y, x + tile_size, y + tile_size) for x, y in itertools.product(xs, ys)]

    extent_morphology = spatialdata.get_extent(sdata["morphology_focus"])
    morphology_focus_bounding_box = shapely.box(
        xmin=min(extent_morphology["x"]),
        ymin=min(extent_morphology["y"]),
        xmax=max(extent_morphology["x"]),
        ymax=max(extent_morphology["y"])
    )

    tiles_in_capture_area = [tile for tile in tiles if morphology_focus_bounding_box.contains(tile)]

    segmentation_ids = []

    def chunk(arr_range, arr_size):
        arr_range = iter(arr_range)
        return iter(lambda: list(islice(arr_range, arr_size)), [])

    batches = list(chunk(tiles_in_capture_area, 100))
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
