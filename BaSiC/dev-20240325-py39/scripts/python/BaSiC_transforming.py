#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 Tong LI <tongli.bioinfo@proton.me>
"""

"""
import fire
from aicsimageio import AICSImage
from aicsimageio.writers import OmeTiffWriter
from ome_zarr.writer import write_image
from ome_zarr.io import parse_url
from ome_zarr.scale import Scaler
import zarr
from aicsimageio import types
from basicpy import BaSiC
import numpy as np
from glob import glob
from typing import List
import json
import logging
import zipfile
from numcodecs import Zlib
import os
from pathlib import Path
logger = logging.getLogger(__name__)


def version() -> str:
    return "0.0.2"


def main(field:str, out_dir:str, format:str=None) -> None:
    """
    Perform BaSiC fitting on a stack of images.
    field : str
        Path to the directory containing the zarr files.
    out_dir : str
        Path to the output directory to save the corrected images.
    """
    logger.info("Load origianl metadata from .zattrs file.")
    original_zattrs = f"{field}/.zattrs"
    with open(original_zattrs) as f:
        config = json.load(f)

    hyperstack = AICSImage(f"./{field}")
    corrected_stack = []
    for t in range(hyperstack.dims.T):
        for c in range(hyperstack.dims.C):
            img = hyperstack.get_image_dask_data("ZYX", T=t, C=c)
            model_p = glob(f"BaSiC_model_F*_C{c}_T*")[0]
            basic = BaSiC.load_model(model_p)
            transformed = basic.transform(img)
            corrected_stack.append(transformed)

    logger.info("Write Zarr file with corrected images.")

    if format == "zip":
        Path(out_dir).parent.mkdir(parents=True)
        # store = zarr.ZipStore(Path(f"test.zip"), compression=zipfile.ZIP_DEFLATED, mode='w')
        store = zarr.ZipStore(out_dir, compression=zipfile.ZIP_STORED, mode='w')
        storage_options = {'compressor': Zlib(level=0)}
    elif format == "tif" or format == "tiff":
        Path(out_dir).parent.mkdir(parents=True)
        OmeTiffWriter.save(np.expand_dims(np.vstack(corrected_stack), 0), out_dir,
            # dim_order=[d["name"] for d in config['multiscales'][0]['axes']]
        )
        return
    else:
        store = parse_url(out_dir, mode="w").store
        storage_options = {}
    root_group = zarr.group(store=store)
    # Pass all metada to the root group
    for k, v in config.items():
        root_group.attrs[k] = v
    # root_group.attrs[".zgroup"] = {"zarr_format" : 2}
    write_image(
        image=np.expand_dims(np.vstack(corrected_stack), 0),
        group=root_group,
        scaler=Scaler(),
        axes=[d["name"] for d in config['multiscales'][0]['axes']],
        storage_options=storage_options,
        # coordinate_transformations=config["multiscales"][0]["datasets"],
    )


if __name__ == "__main__":
    fire.Fire({
        "version": version,
        "run": main
    })