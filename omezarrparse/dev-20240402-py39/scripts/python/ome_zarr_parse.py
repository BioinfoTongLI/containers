#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2024 Tong LI <tongli.bioinfo@proton.me>
"""

"""
import fire
import json
import os
from pathlib import Path
from ome_types import from_xml


def version() -> str:
    return "0.0.1"


def main(zarr_path:str, out_params_json:str) -> None:
    """
    This function parses the OME-Zarr metadata and generates a JSON file with the extracted information.

    :param zarr_path: The path to the OME-Zarr dataset.
    :param params_json: The path to the output JSON file.
    """
    original_path = os.path.realpath(zarr_path)
    ome_me_path = os.path.join(zarr_path, "OME", "METADATA.ome.xml")
    with open(ome_me_path) as f:
        ome_xml = from_xml(f.read())
    pos_md = {}
    pos_md["position_x"] = ome_xml.images[0].pixels.planes[0].position_x
    pos_md["position_y"] = ome_xml.images[0].pixels.planes[0].position_y
    pos_md["position_x_unit"] = ome_xml.images[0].pixels.planes[0].position_x_unit.value
    pos_md["position_y_unit"] = ome_xml.images[0].pixels.planes[0].position_y_unit.value
        
    pixel_size_xy_meta = {"pixel_size": ome_xml.images[0].pixels.physical_size_y, "unit":ome_xml.images[0].pixels.physical_size_y_unit.value}
    chs_meta = [{"name":ch.name, "emission":ch.emission_wavelength} for ch in ome_xml.images[0].pixels.channels]

    with open(os.path.join(zarr_path, "OME", ".zattrs")) as f:
        series = json.load(f)['series']
        metrics = []
        for serie in series:
            metrics.append([{'id': Path(zarr_path).stem}, original_path, serie, chs_meta, pixel_size_xy_meta, pos_md])
    with open(out_params_json, 'w') as f:
        json.dump(metrics, f)
    

if __name__ == "__main__":
    fire.Fire({
        "version": version,
        "run": main
    })