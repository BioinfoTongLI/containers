#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Wellcome Sanger Institute
from spatialdata_io import xenium, xenium_aligned_image
import fire


def harmonise_xenium(
        xenium_folder:str,
        he_image_path:str,
        he_image_alignment_file_path:str):
    sdata = xenium(
        xenium_folder, 
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
    sdata.write(f"{xenium_folder}.zarr", overwrite=True)

    
def main():
    xenium_datasets_with_he_images = {
        "Xenium_Prime_Human_Skin_FFPE_outs":
            [
                "Xenium_Prime_Human_Skin_FFPE_he_image.ome.tif",
                "Xenium_Prime_Human_Skin_FFPE_he_imagealignment.csv"
            ],
        "Xenium_Prime_Human_Prostate_FFPE_outs":
            [
                "Xenium_Prime_Human_Prostate_FFPE_he_image.ome.tif",
                "Xenium_Prime_Human_Prostate_FFPE_he_imagealignment.csv"
            ]
    }
    for xenium_folder, (he_image_path, he_image_alignment_file_path) in xenium_datasets_with_he_images.items():
        harmonise_xenium(
            xenium_folder=f"../{xenium_folder}",
            he_image_path=f"../{he_image_path}",
            he_image_alignment_file_path=f"../{he_image_alignment_file_path}"
        )


if __name__ == "__main__":
    fire.Fire(main)