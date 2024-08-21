#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script will slice the image in XY dimension and save the slices coordinates in json files
"""
import fire
from aicsimageio import AICSImage
import os
from cellpose import core, io, models, denoise
import numpy as np
from shapely import Polygon, wkt, MultiPolygon

import logging

VERSION="0.0.1"


def main(
    image:str,
    x_min:int, x_max:int, y_min:int, y_max:int,
    out_dir:str,
    cell_diameter:int=30,
    cellpose_model:str="cyto3",
    is_3d:bool=False,
    channels:list=[0, 0],
    **cp_params
    ):

    logging.info(f"Loading Cellpose model: {cellpose_model} (GPU: {core.use_gpu()})")
    print(f"Loading Cellpose model: {cellpose_model} (GPU: {core.use_gpu()})")

    model = models.Cellpose(gpu=core.use_gpu(), model_type=cellpose_model)
    # model = denoise.CellposeDenoiseModel(
    #     gpu=core.use_gpu(),
    #     model_type=cellpose_model,
    #     restore_type="denoise_cyto3",
    #     chan2_restore=False
    # )

    img = AICSImage(image)
    ch_ind = channels[0] if len(np.unique(channels)) == 1 else channels
    z = 0 if not is_3d else -1
    lazy_one_plane = img.get_image_dask_data("ZCYX", T=0, C=ch_ind, Z=z)
    crop = np.squeeze(lazy_one_plane[:, :, y_min:y_max, x_min:x_max].compute())
    masks, flows, _, _ = model.eval(
        crop,
        channels=channels,
        diameter=cell_diameter,
        **cp_params,
    )
    os.mkdir(out_dir)
    io.save_masks(
        crop,
        masks,
        flows,
        file_names=out_dir,
        save_txt=True,
        png=True,
        tif=False,
        save_flows=False,
        save_outlines=True,
        savedir=out_dir,
    )
    # convert cellpose outlines to WTK
    logging.info(f"Converting outlines to WKT format")
    outlines_file = os.path.join(out_dir, f"{out_dir}_cp_outlines.txt")
    if os.path.exists(outlines_file):
        wkts = []
        with open(outlines_file, "rt") as f:
            for line in f.readlines():
                # split by comma and make integer
                try:
                    outline = list(map(int, line.strip().split(",")))
                except:
                    continue
                outline = np.array(list(zip(outline[::2], outline[1::2])))
                # transport tile coordinats to original image coordinates
                outline[:, 0] += x_min
                outline[:, 1] += y_min
                poly = Polygon(outline).buffer(0)
                if isinstance(poly, MultiPolygon):
                    poly = poly.geoms[0]
                wkts.append(poly)

        wkt_filename = os.path.join(out_dir, f"{out_dir}_cp_outlines.wkt")
        with open(wkt_filename, "wt") as f:
            f.write(wkt.dumps(MultiPolygon(wkts)))
    else:
        print("No outlines file found")
        with open(os.path.join(out_dir, f"{out_dir}_cp_outlines.wkt"), "wt") as f:
            f.write("")


if __name__ == "__main__":
    options = {
        "run": main,
        "version": VERSION,
    }
    fire.Fire(options)