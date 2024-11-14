#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Wellcome Sanger Institute

import spatialdata as sd
import numpy as np
import fire
import json
import os


VERSION = "0.0.1"
def main(
        sdata:str,
        out_name:str,
        n_partition:int=10,
        element_name:str="cell_boundaries",
         **sdata_kwargs):
    sdata = sd.read_zarr(sdata, sdata_kwargs)
    if not os.path.exists(out_name):
        os.makedirs(out_name)
    if n_partition == 1:
        with open(f"{out_name}/section_0.json", "w") as file:
            json.dump(sdata.shapes[element_name].index.tolist(), file)
    else:
        sections = np.array_split(sdata.shapes[element_name], n_partition)
        indexes = [section.index for section in sections]
        # Serialize indexes into JSON files
        for i, index in enumerate(indexes):
            with open(f"{out_name}/section_{i}.json", "w") as file:
                json.dump(index.tolist(), file)

    

    


if __name__ == '__main__':
    options = {
        "run" : main,
        "version" : VERSION
    }
    fire.Fire(options)