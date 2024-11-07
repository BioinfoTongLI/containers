import uuid
import shapely
import spatialdata
from spatialdata_io import xenium, xenium_aligned_image

from .get_segmentations import get_segmentations
from .register_and_upload_array_file import register_and_upload_array_file
from .register_feature import register_feature


def main(
        xenium_bundle_path: str,
        he_image_path: str,
        he_image_alignment_file_path: str,
        harmonised_dataset_id: str,
        segmentation_flavor_id: str,
        feature_flavor_id: str,
        patch_size: int,
):

    segmentations = get_segmentations(
        harmonised_dataset_id, segmentation_flavor_id
    )

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

    feature_ids = []

    n_segmentations = len(segmentations)

    for i, segmentation in enumerate(segmentations):

        print(f"processing {i} of {n_segmentations} segmentations")

        seg_id, seg_polygon = segmentation

        # generate the features with uuids
        feat_id = uuid.uuid4()
        feat_file_id = uuid.uuid4()

        # generate a query area for extracting the patch
        x, y = seg_polygon.centroid.coords[0]
        patch_box = shapely.box(
            xmin=(x - (patch_size / 2)),
            xmax=(x + (patch_size / 2)),
            ymin=(y - (patch_size / 2)),
            ymax=(y + (patch_size / 2))
        )

        # make a spatial query against the spatialdata object
        image_feature_xarray = spatialdata.polygon_query(
            sdata["histology"],
            patch_box,
            target_coordinate_system="global")

        array_file_id = register_and_upload_array_file(
            array=image_feature_xarray,
            array_dimensions=["c", "x", "y"],
        )

        feature_id = register_feature(
            segmentation_id=seg_id,
            array_file_id=array_file_id,
            feature_flavor_id=feature_flavor_id,
        )

        feature_ids.append(feature_id)

    return feature_ids
