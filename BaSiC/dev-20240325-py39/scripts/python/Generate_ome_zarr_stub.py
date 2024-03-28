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


def version() -> str:
    return "0.0.1"


def parse_metadata(zarr_path):
    """
    Parse metadata from a given Zarr path.

    This function reads an OME-XML file to get the number of channels, reads a couple of JSON files, 
    and then constructs a list of metrics based on the contents of those files.

    :param zarr_path: The path to the Zarr file.
    :type zarr_path: str
    :return: A list of metrics.
    :rtype: list
    """
    original_path = os.path.realpath(zarr_path)
    # Read the OME-XML file to get the number of channels.
    with open(os.path.join(zarr_path, "OME", "METADATA.ome.xml")) as f:
        ome_xml = from_xml(f.read())

    n_channel = ome_xml.images[0].pixels.size_c
    channel_indexes = list(range(n_channel))

    timepoints = 0  # not fully supported for bespoke values

    with open(os.path.join(zarr_path, ".zattrs")) as f:
        md = json.load(f)
    with open(os.path.join(zarr_path, "OME", ".zattrs")) as f:
        series = json.load(f)['series']
    metrics = []
    if md.get('plate') is None:
        for serie in series:
            for ch in channel_indexes:
                metrics.append([{'id': Path(zarr_path).stem}, original_path, -1, ch, timepoints, serie])
    else:
        for serie in series:
            row, col, field = serie.split("/")
            rela_path = os.path.join(row, col)
            for ch in channel_indexes:
                metrics.append([{'id': Path(zarr_path).stem}, original_path, int(field), ch, timepoints, rela_path])
    return metrics
    

def main(zarr_in:str, out_zarr_name:str, out_fov_json:str) -> None:
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
    metrics = parse_metadata(zarr_in)
    # Save metrics as JSON
    with open(out_fov_json, 'w') as f:
        json.dump(metrics, f)


if __name__ == "__main__":
    fire.Fire({
        "version": version,
        "run": main
    })