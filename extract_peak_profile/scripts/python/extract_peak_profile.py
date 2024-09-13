#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Wellcome Sanger Institute

from aicsimageio import AICSImage
import pandas as pd
from skimage.morphology import disk
import fire
import numpy as np
from shapely import from_wkt, MultiPoint
from tqdm import tqdm


VERSION = "0.0.1"

def make_in_range(l, upper):
    l = np.where(l < 0, 0, l)
    l = np.where(l > upper, upper, l)
    return l


def main(image:str, peaks:str, stem:str,
         pixelsize:float=1.0, peak_radius:int=4,
         y_col:str='y_int',
         x_col:str='x_int'):
    print('Reading image and transcripts')
    if peaks.endswith('.csv'):
        spots = pd.read_csv(peaks, header=0, sep=',')[[y_col, x_col]].values
    elif peaks.endswith('.tsv'):
        spots = pd.read_csv(peaks, header=0, sep='\t')[[y_col, x_col]].values
    elif peaks.endswith('.wkt'):
        # Assuming that the wkt file contains a multipoint geometry
        with open(peaks, 'r') as f:
            multispots = from_wkt(f.read())
        if not isinstance(multispots, MultiPoint):
            raise ValueError('Please provide a wkt file with multipoint geometry')
        spots = np.array([(geom.y, geom.x) for geom in multispots.geoms])
    else:
        raise ValueError('Format not recognized. Please provide a csv, tsv or wkt file')

    # Convert the coordinates to pixel coordinates
    spots = (spots/pixelsize).astype(np.int32)
    
    # Get pixel data
    image = AICSImage(image)
    image_stack = image.get_image_dask_data("CYX")
    img_Y, img_X = image_stack.shape[-2:]
    print(image_stack)

    # Get the cooridnates of pixels surrounding the peaks 
    disk_img = disk(peak_radius)
    indices = np.where(disk_img == 1)
    dXYpair = zip(indices[0] - peak_radius, indices[1] - peak_radius)

    # Translate the coordinates of the peaks to the coordinates of the pixels surrounding the peaks
    Xs, Ys = [], []
    for dx, dy in dXYpair:
        Ys.append(make_in_range(spots[:,0] + dy, img_Y - 1))
        Xs.append(make_in_range(spots[:,1] + dx, img_X - 1))

    peak_intensities = []
    # Using for loop here to save memory, since dask doesnt' support fancy indexing yet.
    # Otherwise we would use broadcasting to get the peak profiles
    for ch in tqdm(range(image_stack.shape[0])):
        peak_profile_surroundings = image_stack[ch].compute()[Ys, Xs]
        max_intensity = np.max(peak_profile_surroundings, axis=0)
        peak_intensities.append(max_intensity)
    formatted_peak_profiles = np.array(peak_intensities).astype(np.int32)
    print(formatted_peak_profiles.shape)
    np.save(
        f"{stem}.npy",
        formatted_peak_profiles,
        allow_pickle=True,
    )
    pd.DataFrame(spots, columns=["y_int", "x_int"]).to_csv(f"{stem}_locations.csv", index=False)
        
    
if __name__ == "__main__":
    options = {
        "run": main,
        "version": VERSION
    }
    fire.Fire(options)