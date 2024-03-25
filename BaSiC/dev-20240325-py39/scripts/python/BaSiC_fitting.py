#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 Tong LI <tongli.bioinfo@proton.me>
"""

"""
import fire
from aicsimageio import AICSImage
from basicpy import BaSiC
import numpy as np
from glob import glob
import logging
from pathlib import Path
logger = logging.getLogger(__name__)


def version() -> str:
    return "0.1.0"


def main(zarr:str, C:int, field:str, out:str, T:int=1, basic_options:dict={}) -> None:
    """
    Fit the BaSiC model to the given zarr dataset.

    Parameters:
    ----------
    zarr : str
        Path to the zarr dataset.
    C : int
        Number of channels.
    field : str
        Field of view to process.
    out : str
        Path to save the fitted model.
    T : int, optional
        Number of timepoints. Default is 1.
    basic_options : dict, optional
        Additional options for BaSiC fitting. Default is an empty dictionary.

    Returns:
    -------
    None
    """
    
    if field >= 0: 
        # This implies HCS plate with more than 1 field of view per well
        # Populate stack across all wells for the given position (field)
        # So the model will be position specific
        fovs = glob(f"{zarr}/*/*/{field}")
    else:
        # Filter directories that are only digits and excluse OME directory with metadata
        fovs = [d for d in glob(f"{zarr}/*") if d.split("/")[-1] != "OME"]

    n_fov = len(fovs)
    # Use all (or part) or the positions to fit the model
    if n_fov > 500:
        n = len(fovs) // 100
        logger.info(f"Too many positions to fit the model. Use only around 100 of the positions.")
    else:
        logger.info(f"Use all positions to fit the model.")
        n = 1

    stack = []
    for f in fovs[::n]:
        stack.append(AICSImage(f).get_image_dask_data("ZYX", S=0, T=T, C=C))
    stack_np = np.array(stack)
    logger.info(stack_np.shape)

    basic = BaSiC(get_darkfield=True, **basic_options)
    basic.fit(stack_np.astype(np.int16))
    basic.save_model(out)


if __name__ == "__main__":
    fire.Fire({
      'run': main,
      'version': version,
    })