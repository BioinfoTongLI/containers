#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Wellcome Sanger Institute

"""

"""
import fire
from aicsimageio import AICSImage
from spotiflow.model import Spotiflow
import csv
import os
import numpy as np


def main(image_path:str, out_dir:str, out_name:str,
         x_min:int, x_max:int, y_min:int, y_max:int,
         ch_ind:int=2, model_name:str="general",
         zs:list=[0]):
    img = AICSImage(image_path)
    lazy_one_plane = img.get_image_dask_data(
        "ZCYX",
        T=0, # only one time point is allowed for now
        C=ch_ind,
        Z=zs)
    crop = lazy_one_plane[:, :, y_min:y_max, x_min:x_max].squeeze().compute()
    model = Spotiflow.from_pretrained(model_name)
    peaks, details  = model.predict(crop)

    # Create the output directory if it doesn't exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(f"{out_dir}/{out_name}", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['y', 'x'])  # write column names
        if len(peaks) > 0:
            # Serialize peaks to disk as CSV
            peaks[:, 0] = peaks[:, 0] + y_min
            peaks[:, 1] = peaks[:, 1] + x_min 
            writer.writerows(peaks)


if __name__ == "__main__":
    options = {
        "run" : main,
        "version" : "0.0.1"
    }
    fire.Fire(options)
