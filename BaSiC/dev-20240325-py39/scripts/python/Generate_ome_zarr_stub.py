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


def version() -> str:
    return "0.0.1"


def main(zarr_in:str, out_zarr_name:str) -> None:
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


if __name__ == "__main__":
    fire.Fire({
        "version": version,
        "run": main
    })