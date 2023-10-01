#!/usr/bin/env python3

import io
import os
import pathlib

import argparse

import xml.etree.ElementTree as ET

from wgrd_cons_tools.utils import *
from wgrd_cons_tools.helper_dds import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=pathlib.Path, help="path to the tgv xml file")
    parser.add_argument("-o", "--output", type=pathlib.Path, default="./out/",
                        help="path to the output directory")
    args = parser.parse_args()

    abs_path = os.path.dirname(os.path.abspath(args.path))

    xml = ET.parse(args.path)
    root = xml.getroot()

    compressed = root.attrib["compressed"]
    width = int(root.attrib["width"])
    height = int(root.attrib["height"])
    format = root.attrib["pixelFormatName"]

    mipmaps = []
    for c in root:
        if c.tag == "mipmap":
            mipmaps.append(c.attrib["data"])
        else:
            print("Unknown tag in xml: %s" % c.tag)

    dds_mipmaps = []
    # tgv mipmap order is exactly the opposite of DDS mipmap order
    for mipmap in mipmaps[::-1]:
        filestream = open(os.path.join(abs_path, mipmap), "rb")
        if compressed == "compressed":
            zipo = filestream.read(4)
            assert(zipo == b"ZIPO")
            uncompressedSize = read32(filestream)
            compressedData = filestream.read()
            uncompressedData = decompress_zlib(compressedData)
            assert(len(uncompressedData) == uncompressedSize)
            stream = io.BytesIO(uncompressedData)
        else:
            stream = filestream

        dds_mipmaps.append(stream)

        #transformedData = uncompressedData
        #if ddsFormat[1] != None:
        #    transformedData = ddsFormat[1](transformedData)

    outfile = open(os.path.join(args.output, os.path.basename(args.path) + ".dds"), "wb")
    stream_write_dds(outfile, width, height, format, dds_mipmaps)
