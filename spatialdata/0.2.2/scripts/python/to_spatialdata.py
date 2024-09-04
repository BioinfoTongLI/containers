#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Wellcome Sanger Institute

from spatialdata_io import xenium
import fire

VERSION = "0.0.1"
def main(xenium_input:str, out_name:str):
    xenium.xenium(xenium_input).write(out_name)

if __name__ == '__main__':
    options = {
        "run" : main,
        "version" : VERSION
    }
    fire.Fire(options)