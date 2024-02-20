import pathlib
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("wgrd_exe", type=pathlib.Path,
                        help="path to the vanilla Wargame3.exe")
    parser.add_argument("-r", "--revision", type=int, default=80001)
    parser.add_argument("-o", "--output", default="out/Wargame3_modded.exe", type=pathlib.Path,
                        help="path to the output Wargame3.exe")
    args = parser.parse_args()

    position = 0x01520213

    with open(args.output, "wb") as patched:
        with open(args.wgrd_exe, "rb") as original:
            patched.write(original.read(position))
            original_revision = original.read(10)
            new_revision = str(args.revision)
            assert(len(new_revision) <= 10)
            new_revision = (10-len(new_revision)) * "0" + new_revision

            patched.write(new_revision.encode("ascii"))
            patched.write(original.read())
