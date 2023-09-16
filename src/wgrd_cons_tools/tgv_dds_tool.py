import pdb

import os
import pathlib

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=pathlib.Path, help="path to the tgv output image file")
    parser.add_argument("-o", "--output", type=pathlib.Path, default="./out/",
                        help="path to the output directory")
    args = parser.parse_args()



    pdb.set_trace()