#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import fire
import pandas as pd
import re
import numpy as np
from collections import OrderedDict


VERSION = "0.0.1"
"""
Example of Cartana codebook:

gene,code,cycle1_channel1_AF750,cycle1_channel2_Cy5,cycle1_channel3_Cy3,cycle1_channel4_AF488,cycle1_channel5_DAPI,cycle2_chann
el1_AF750,cycle2_channel2_Cy5,cycle2_channel3_Cy3,cycle2_channel4_AF488,cycle2_channel5_DAPI,cycle3_channel1_AF750,cycle3_chann
el2_Cy5,cycle3_channel3_Cy3,cycle3_channel4_AF488,cycle3_channel5_DAPI,cycle4_channel1_AF750,cycle4_channel2_Cy5,cycle4_channel
3_Cy3,cycle4_channel4_AF488,cycle4_channel5_DAPI,cycle5_channel1_AF750,cycle5_channel2_Cy5,cycle5_channel3_Cy3,cycle5_channel4_
AF488,cycle5_channel5_DAPI,cycle6_channel1_AF750,cycle6_channel2_Cy5,cycle6_channel3_Cy3,cycle6_channel4_AF488,cycle6_channel5_
DAPI
ACTG2,442412,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0
APLNR,341231,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0
"""
def main(csv_file,
         channel_map:dict={"Cy5": "A", "AF488": "G", "Cy3": "C", "Atto425": "T", "AF750":"T"}, # This is orderd! be cautious !!!
         sep=","):
    channel_map = OrderedDict(channel_map)
    print(channel_map)
    if csv_file.endswith(".xlsx"):
        d = pd.read_excel(csv_file)
    else:
        d = pd.read_csv(csv_file, sep=sep)
    code_sizes = [len(str(c)) for c in d.code]
    n_cycle_list = np.unique(code_sizes)
    assert len(n_cycle_list) == 1
    channel_info = {}
    channel_info["nCycles"] = n_cycle_list[0]

    channel_dict = {}
    for col in d.columns:
        if col.startswith("cycle"):
            m = re.search("cycle(\d+)_channel(\d+)_(.*)", col)
            channel_dict[(m.group(1), m.group(2))] = m.group(3)
    nucleotide_codes = []
    for gene_ind in d.index:
        gene = d.loc[gene_ind]
        str_l = []
        for i, ind in enumerate(str(gene.code)):
            ch_name = channel_dict[(str(i + 1), ind)]
            col_name = f"cycle{i+1}_channel{ind}_{ch_name}"
            assert gene[col_name] == 1
            str_l.append(ch_name)
        nucleotids = "".join([channel_map[s] for s in str_l])
        nucleotide_codes.append(nucleotids)
    d["nucleotide_codes"] = nucleotide_codes
    channel_indexes = [int(k[1]) for k in channel_dict.keys()]
    assert len(np.unique(channel_indexes)) == np.max(channel_indexes)
    channel_info["nChannel"] = np.max(channel_indexes)
    channel_info["DAPI"] = "nuclei"
    for ch in channel_map:
        if ch == "AF750":
            channel_info["Atto425"] = channel_map[ch]
        else:
            channel_info[ch] = channel_map[ch]

    df = pd.DataFrame(pd.Series(channel_info)).T
    df.to_csv("channel_info.csv", index=False)
    print(df)

    taglist = d[["gene", "nucleotide_codes"]]
    taglist = taglist.rename(columns={"gene": "Gene", "nucleotide_codes": "Channel"})
    print(taglist)
    pd.DataFrame(taglist).to_csv("taglist.csv", index=False)


if __name__ == "__main__":
    options = {
        "run": main,
        "version": VERSION 
    }
    fire.Fire(options)
