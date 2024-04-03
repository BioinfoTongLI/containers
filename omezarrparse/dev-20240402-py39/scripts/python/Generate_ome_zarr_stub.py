#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2024 Tong LI <tongli.bioinfo@proton.me>
"""

"""
import fire
import shutil
import json
import os
from pathlib import Path
from ome_types import from_xml


def main(zarr_in:str, out_zarr_name:str, out_fov_json:str) -> None:
    """
    Generate OME-Zarr stub.

    This function generates an OME-Zarr stub by copying necessary files and directories from the input
    OME-Zarr dataset to the output directory. It also creates a JSON file containing parameters for downstream
    processing.

    Args:
        zarr_in (str): Path to the input OME-Zarr dataset.
        out_zarr_name (str): Path to the output directory where the OME-Zarr stub will be generated.
        out_fov_json (str): Path to the output JSON file containing parameters for downstream processing.

    Returns:
        None
    """
    original_path = os.path.realpath(zarr_in)
    with open(Path(zarr_in) / ".zattrs") as f:
        data = json.load(f)
    
    shutil.copytree(f"{zarr_in}/OME", f"{out_zarr_name}/OME")
    shutil.copy(f"{zarr_in}/.zattrs", f"{out_zarr_name}/.zattrs")
    shutil.copy(f"{zarr_in}/.zgroup", f"{out_zarr_name}/.zgroup")
    if 'plate' in data.keys():
        for w in data["plate"]["wells"]:
            row, col = w["path"].split("/")
            os.makedirs(f"{out_zarr_name}/{row}/{col}") 
            shutil.copy(f"{zarr_in}/{row}/.zgroup", f"{out_zarr_name}/{row}/.zgroup")
            shutil.copy(f"{zarr_in}/{row}/{col}/.zattrs", f"{out_zarr_name}/{row}/{col}/.zattrs")
            shutil.copy(f"{zarr_in}/{row}/{col}/.zgroup", f"{out_zarr_name}/{row}/{col}/.zgroup")
    with open(Path(zarr_in) / "OME" / ".zattrs") as f:
        series = json.load(f)
    params_for_downstream = []
    for s in series['series']:
        params_for_downstream.append([{'id': Path(zarr_in).stem}, original_path, s, out_zarr_name])    

    # Save metrics as JSON
    with open(out_fov_json, 'w') as f:
        json.dump(params_for_downstream, f)


if __name__ == "__main__":
    fire.Fire({
        "version": "0.0.1",
        "run": main
    })