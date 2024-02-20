from wgrd_cons_parsers.edat import EDat

import os, pathlib
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--wgrd_path", type=pathlib.Path,
                        help="path to the vanilla game files, e.g. C:/Program Files (x86)/Steam/steamapps/common/Wargame Red Dragon/Data/WARGAME/PC")
    parser.add_argument("-m", "--modded_path", type=pathlib.Path,
                        help="path to the modded game files")
    parser.add_argument("-o", "--output", default="out/", type=pathlib.Path,
                        help="path to the output directory")
    args = parser.parse_args()

    output_edat_files = {}

    for root, dirs, files in os.walk(args.modded_path):
        for file in files:
            if file.endswith(".dat"):
                rel_root = os.path.relpath(root, args.modded_path)
                rel_filepath = os.path.join(rel_root, file)
                original_filepath = os.path.join(args.wgrd_path, rel_filepath)
                modded_filepath = os.path.join(args.modded_path, rel_filepath)

                print("parsing file: ", modded_filepath)

                extra = {"_cons_xml_filesdictionary_alignment": False,
                         "_cons_xml_filesdictionary_disable_checks": True}
                original_edat = EDat.parse_file(original_filepath, **extra)
                modded_edat = EDat.parse_file(modded_filepath, **extra)

                output_edat_file = output_edat_files.get(file, {"sectorSize": original_edat["sectorSize"], "files": {}})
                for k, v in modded_edat["files"].items():
                    if k in original_edat["files"]:
                        if v != original_edat["files"][k]:
                            print(k)
                            output_edat_file["files"][k] = v
                        #else:
                        #    output_edat_file["files"][k] = v
                output_edat_files[file] = output_edat_file

    os.makedirs(args.output, exist_ok=True)
    for k, v in output_edat_files.items():
        preprocessed, _ = EDat.preprocess(v)
        output_edat = EDat.build_file(preprocessed, os.path.join(args.output, k))

