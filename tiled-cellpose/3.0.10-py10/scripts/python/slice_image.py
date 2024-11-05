#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Wellcome Sanger Institute
"""
This script will slice the image in XY dimension and save the slices coordinates in json files
"""
import fire
from aicsimageio import AICSImage
import json
import csv
import os


VERSION="0.0.1"


def calculate_slices(image_size, chunk_size, overlap):
    width, height = image_size
    slices = []
    for i in range(0, width, chunk_size - overlap):
        for j in range(0, height, chunk_size - overlap):
            box = (i, j, min(i + chunk_size, width), min(j + chunk_size, height))
            slices.append(box)
    return slices


'''
Deprecating this function as it will duplicate the data and not used in the main function
'''
# def save_chunk_locations(arr, block_info, block_id, out_folder, overlap):
#     print(block_id)
#     array_loc = "_".join([str(i) for i in block_info[0]["array-location"]])
#     file_name = f"{out_folder}/{array_loc}.json"
#     print(file_name)
#     # Remove 'dtype' from block_info
#     del block_info[None]['dtype']
#     block_info["overlap"] = overlap
#     with open(file_name, "w") as f:
#         json.dump(block_info, f)
#     return arr


def main(image:str, out:str, overlap:int=30, chunk_size:int=4096, out_name:str="tile_coords.csv"):
    img = AICSImage(image)
    lazy_one_plane = img.get_image_dask_data("XY")
    slices = calculate_slices(lazy_one_plane.shape, chunk_size, overlap)
    os.mkdir(out)
    # Create a CSV file to write the slices
    csv_file = f"{out}/{out_name}"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Tile", "X1", "Y1", "X2", "Y2"])  # Write header

        # Write each slice to the CSV file
        for i, slice in enumerate(slices):
            x1, y1, x2, y2 = slice
            writer.writerow([i+1, x1, y1, x2, y2])


if __name__ == "__main__":
    options = {
        "run": main,
        "version": VERSION,
    }
    fire.Fire(options)
