#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
Read metadata for decoding
"""
# from reading_data_functions import read_taglist_and_channel_info
from pandas import read_csv
import numpy as np
import pickle
import fire

VERSION = "0.0.1"


# auxiliary functions required for reading and handling the data
def barcodes_01_from_channels_1234(barcodes_1234, C, R):
    K = barcodes_1234.shape[0]
    barcodes_01 = np.ones((K, C, R))
    for b in range(K):
        barcodes_01[b, :, :] = 1 * np.transpose(
            barcodes_1234[b, :].reshape(R, 1) == np.arange(1, C + 1)
        )
    return barcodes_01


def barcodes_01_from_letters(barcodes_AGCT, barcode_letters, R):
    K = len(barcodes_AGCT)
    C = len(barcode_letters)
    barcodes_1234 = np.zeros((K, R))
    for k in range(K):
        for r in range(R):
            barcodes_1234[k, r] = (
                np.where(barcode_letters == barcodes_AGCT[k][r])[0][0] + 1
            )
    barcodes_01 = barcodes_01_from_channels_1234(barcodes_1234, C, R)
    return barcodes_01


def read_taglist_and_channel_info(
    data_path, taglist_name="taglist.csv", channel_info_name="channel_info.csv"
):
    # reads taglist.csv and channel_info.csv and
    # returns barcodes_01 which is a numpy array with 01 entries and dimension K x C x R
    taglist = read_csv(data_path + taglist_name)
    channel_info = read_csv(data_path + channel_info_name)
    gene_names = np.array(taglist.Gene)
    barcodes_AGCT = np.array(taglist.Channel)

    K = len(taglist)  # number of barcodes
    R = channel_info.nCycles[0]  # number of rounds
    C_total = channel_info.nChannel[0]

    channel_base = []
    coding_chs = []
    channel_names = []
    for i in range(C_total):
        name = channel_info.columns[2 + i]
        base = channel_info.iloc[:, 2 + i][0]
        coding_chs.append(len(base) == 1)
        channel_base.append(base)
        channel_names.append(name)

    C = sum(coding_chs)  # number of coding channels
    barcode_letters = np.array(channel_base)[np.array(coding_chs)]
    barcodes_01 = barcodes_01_from_letters(barcodes_AGCT, barcode_letters, R)

    channels_info = dict()
    for key in ["barcodes_AGCT", "coding_chs", "channel_base", "channel_names"]:
        channels_info[key] = locals()[key]
    return barcodes_01, K, R, C, gene_names, channels_info


def main(auxillary_file_dir, taglist_name, channel_info_name):
    # read channel_info.csv and taglist.csv
    barcodes_01, K, R, C, gene_names, channels_info = read_taglist_and_channel_info(
        auxillary_file_dir,
        taglist_name=taglist_name,
        channel_info_name=channel_info_name,
    )

    np.save("barcodes_01.npy", barcodes_01)
    np.save("gene_names.npy", gene_names)
    channels_info["K"] = K
    channels_info["R"] = R
    channels_info["C"] = C
    with open("channel_info.pickle", "wb") as fp:
        pickle.dump(channels_info, fp)


if __name__ == "__main__":
    options = {
        "run": main,
        "version": VERSION,
    }
    fire.Fire(options)
