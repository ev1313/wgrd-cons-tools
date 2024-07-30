#!/usr/bin/env python3

import os
import sys
import argparse
import pathlib

from wgrd_cons_parsers.edat import EDat


def create_vfs(dat_file_paths: list[str], vfs_dict: dict[str, pathlib.Path] = None) -> dict[str, pathlib.Path]:
    """
    Create a virtual file system from a list of dat files.
    :param dat_file_paths: list of dat files to be searched
    :param vfs_dict: vfs_dict to be appended to, so it is possible to chain multiple create_vfs calls
    :return: vfs_dict containing all the vfs filepaths from the dat files
    """
    if vfs_dict is None:
        vfs_dict = {}

    idx = 0
    for filepath in dat_file_paths:
        print(f"parsing {filepath}")
        data = EDat.parse_file(filepath, _cons_xml_filesdictionary_parse_files=False)
        for vfspath, meta in data.files.items():
            vfs_dict[vfspath] = (os.path.abspath(filepath), meta.offset + data.offset_data, meta.size, meta.checksum, idx)
            idx += 1

    return vfs_dict


def get_dat_paths(wgrd_path: pathlib.Path) -> list[str]:
    """
    Recursively search for .dat files in the wgrd_path directory.
    :param wgrd_path: Path to the directory containing all the dat files
    :return: list of dat files, sorted by name
    """
    dat_file_paths = []

    for root, dirs, files in os.walk(wgrd_path):
        for file in files:
            if file.endswith(".dat"):
                filepath = os.path.join(root, file)
                dat_file_paths.append(filepath)

    return sorted(dat_file_paths)


def create_vfs_tree(vfs_dict: dict[str, pathlib.Path]) -> dict:
    """
    Create a vfs tree from a vfs_dict.
    :param vfs_dict: vfs_dict mapping vfs paths to dat filepaths
    :return: nested directory structure of the vfs mapping to dat filepaths in the end
    """
    vfs_tree = {}

    for vfs_path, fs_path in vfs_dict.items():
        parts = vfs_path.split("\\")
        last = vfs_tree
        for part in parts[:-1]:
            last.setdefault(part, {})
            last = last[part]
        last[parts[-1]] = fs_path
    
    return vfs_tree


def search_vfs_tree(vfs_dict: dict[str, pathlib.Path], search_string: str) -> dict:
    """
    Search a vfs dict (not the tree) for a search string.
    :param vfs_dict:
    :param search_string:
    :return: a vfs_tree only containing the paths that contain the search string
    """
    search_string.strip()
    search_string = search_string.replace("\\", "/")
    return {k: v for k, v in vfs_dict.items() if search_string in k.replace("\\", "/")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("wgrd_path", type=pathlib.Path, help="path to the wgrd game files")
    #parser.add_argument("output_path", type=pathlib.Path, help="unpack directory", nargs='?', default="./out/")

    args = parser.parse_args()

    print(create_vfs_tree(create_vfs(get_dat_paths(args.wgrd_path))))
