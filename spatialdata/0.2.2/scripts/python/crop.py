#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Wellcome Sanger Institute

import spatialdata as sd
import fire
import json
import os
from tqdm import tqdm

VERSION = "0.0.1"

def main(
        sdata:str,
        index_json:str,
        out_name:str,
        element_name:str,
        **sdata_kwargs
    ):
    sdata = sd.read_zarr(sdata, sdata_kwargs)
    sdata = sdata.subset(["morphology_focus", "cell_labels", element_name])
    indexes = json.loads(open(index_json).read())
    if not os.path.exists(out_name):
        os.makedirs(out_name)
    for i in tqdm(indexes):
        bbox = sdata.shapes[element_name].loc[i].iloc[0].bounds
        sdata_cropped = sd.bounding_box_query(
            sdata, ["x","y"],
            min_coordinate=[bbox[0],bbox[1]],
            max_coordinate=[bbox[2],bbox[3]],
            filter_table=True,
            target_coordinate_system="global")
        sdata_cropped.write(f"{out_name}/sdata_subset_{i}.sdata", overwrite=True)
    

if __name__ == '__main__':
    options = {
        "run" : main,
        "version" : VERSION
    }
    fire.Fire(options)