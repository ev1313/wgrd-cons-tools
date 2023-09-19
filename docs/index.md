# Wargame: Red Dragon Tools

This is a collection of tools for modding Wargame: Red Dragon, a game from Eugen Systems.
These tools use the parsers found in [wgrd-cons-parsers](https://github.com/ev1313/wgrd_cons_parsers) and usually
work on the XML generated from them or just directly use them in Python.

## Usage

You can use these tools in differing ways.
There are prebuilt binaries created by the GitHub Actions and attached to every release.

In this case you can just use the provided binaries directly, for example for unpacking an edat file:

```
edat.exe \path\to\file.edat -o out\
```

If you want to install the Python scripts and use Python directly (recommended, if you want to develop scripts yourself), first install them:

``` bash
    pip install wgrd_cons_parsers wgrd_cons_tools
```

Now you can use for example the edat parser with:

``` bash
python -m wgrd_cons_parsers.edat /path/to/file -o out/
```

Or the encode\_ess tool with:

``` bash
python -m wgrd_cons_tools.encode_ess /path/to/wav -o out/out.ess
```


## Performance

Currently unpacking the everything.ndfbin uses about 14 GB of RAM and takes about 2 minutes on my machine.

It is recommended to use the pypy3 Python runtime, because it significantly increases the performance:

https://www.pypy.org/

## Development

If you want to use the scripts with local modifications easily, you can install them locally:

``` sh
git clone https://github.com/ev1313/wgrd-cons-tools.git
cd wgrd-cons-tools
pip install -e .

```

With this setup you can modify the scripts and still use them.
