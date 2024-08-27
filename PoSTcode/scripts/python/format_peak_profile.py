#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import fire
import pandas as pd
import numpy as np


VERSION = "0.0.1"

def main(csv_file:str, peak_profile_p:str, channel_info_p:str, sep=","):
    channel_info = np.load(channel_info_p, allow_pickle=True)
    if csv_file.endswith(".xlsx"):
        codebook = pd.read_excel(csv_file)
    else:
        codebook = pd.read_csv(csv_file, sep=sep)
    print(codebook)
    spot_profile = np.load(peak_profile_p)
    if len(spot_profile.shape) == 2:
        # if the spot_profile is two dimensional, it is assumed that the spot_profile is in
        # the shape of (n_channel*n_cycle, n_spot). Then reshape it.
        n_spots = spot_profile.shape[-1]
        # fine DAPI/Hoechst channel indexes and remove them from the profile
        coding_ch_mask = channel_info["coding_chs"] * channel_info["R"]
        formatted_spot_profile = spot_profile[coding_ch_mask].reshape(-1, channel_info["R"], n_spots)
    else:
        formatted_spot_profile = spot_profile
    np.save("formatted_spot_profile.npy", formatted_spot_profile)


if __name__ == "__main__":
    options = {
        "run": main,
        "version": VERSION 
    }
    fire.Fire(options)
