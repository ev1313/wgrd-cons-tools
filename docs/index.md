# Wargame Red Dragon Tools

This is a collection of tools for modding Wargame: Red Dragon.
These tools use the parsers found in wgrd-cons-parsers and usually
work on the XML generated from them or just directly use them in Python.

## Usage

``` sh
pip install wgrd_cons_tools


```

## Performance

Currently unpacking the everything.ndfbin uses about 14 GB of RAM and takes about 2 minutes on my machine.

It is recommended to use the pypy3 Python runtime, because it significantly increases the performance:

https://www.pypy.org/

## Development

If you want to change the scripts easily, you can install them locally:

``` sh
git clone https://github.com/ev1313/wgrd-cons-tools.git
cd wgrd-cons-tools
pip install -e .

```

With this setup you can modify the scripts and still use them.
