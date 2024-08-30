#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Wellcome Sanger Institute
from aicsimageio import AICSImage
import pandas as pd
import fire
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

VERSION = "0.0.1"

def main(label_image:str, transcripts:str, out_name:str,
         pixelsize:int=1,
         y_col:str='y_location',
         x_col:str='x_location',
         feature_col:str='feature_name',
    ):
    logger.info('Reading image and transcripts')
    if transcripts.endswith('.csv'):
        spots = pd.read_csv(transcripts, header=0, sep=',')[[y_col, x_col, feature_col]]
    elif transcripts.endswith('.tsv'):
        spots = pd.read_csv(transcripts, header=0, sep='\t')[[y_col, x_col, feature_col]]
    elif transcripts.endswith('.wkt'):
        from shapely import from_wkt, MultiPoint
        # Assuming that the wkt file contains a multipoint geometry
        with open(transcripts, 'r') as f:
            multispots = from_wkt(f.read())
        if not isinstance(multispots, MultiPoint):
            raise ValueError('Please provide a wkt file with multipoint geometry')
        spots = pd.DataFrame([(geom.y, geom.x) for geom in multispots.geoms], columns=[y_col, x_col])
        spots["feature_name"] = 'spot'
    else:
        raise ValueError('Format not recognized. Please provide a csv, tsv or wkt file')
    if label_image.endswith('.tiff') or label_image.endswith('.tif'):
        lab_2D = AICSImage(label_image)
    else:
        raise ValueError('Format not recognized. Please provide a tiff file')
    logger.info('Assigning spots to cells')
    cell_id = lab_2D.dask_data[spots["y_location"].astype(int)/pixelsize, spots["x_location"].astype(int)/pixelsize]
    spots['cell_id'] = cell_id
    logger.info("Create count matrix and save to file")
    count_matrix = spots.pivot_table(index='cell_id', columns='feature_name', aggfunc='size', fill_value=0)
    count_matrix = count_matrix.drop(count_matrix[count_matrix.index == 0].index)
    count_matrix.to_csv(out_name)
        
    
if __name__ == "__main__":
    options = {
        "run": main,
        "version": VERSION
    }
    fire.Fire(options)
        
    
