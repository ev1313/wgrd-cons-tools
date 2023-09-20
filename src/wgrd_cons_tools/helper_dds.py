from typing import IO

from wgrd_cons_tools.utils import *


def stream_write_dds(stream: IO[bytes], w: int, h: int, format: str, mipmaps: list[IO[bytes]]):
    # FIXME: put these in enum?
    DXGI_FORMAT_R16_UNORM = 56
    DXGI_FORMAT_R8_TYPELESS = 60
    DXGI_FORMAT_BC1_UNORM = 71
    DXGI_FORMAT_BC1_UNORM_SRGB = 72
    DXGI_FORMAT_BC3_TYPELESS = 76
    DXGI_FORMAT_BC3_UNORM = 77
    DXGI_FORMAT_BC3_UNORM_SRGB = 78
    DXGI_FORMAT_B8G8R8A8_UNORM = 87
    DXGI_FORMAT_B8G8R8A8_UNORM_SRGB = 91

    # these are specific to the game
    ddsFormats = {
        "DXT1": (DXGI_FORMAT_BC1_UNORM, None),
        "DXT1_SRGB": (DXGI_FORMAT_BC1_UNORM_SRGB, None),
        "DXT5": (DXGI_FORMAT_BC3_TYPELESS, None),
        "DXT5_LIN": (DXGI_FORMAT_BC3_UNORM, None),
        "DXT5_SRGB": (DXGI_FORMAT_BC3_UNORM_SRGB, None),
        'L8': (DXGI_FORMAT_R8_TYPELESS, None),
        "L16_LIN": (DXGI_FORMAT_R16_UNORM, None),
        "A8R8G8B8_LIN": (DXGI_FORMAT_B8G8R8A8_UNORM, None),
        'A8R8G8B8_SRGB': (DXGI_FORMAT_B8G8R8A8_UNORM_SRGB, None)
    }
    ddsFormat = ddsFormats[format]

    # Write https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dds-header

    # FIXME: put these in enum?
    DDSD_CAPS = 0x1
    DDSD_HEIGHT = 0x2
    DDSD_WIDTH = 0x4
    DDSD_PIXELFORMAT = 0x1000
    DDSD_MIPMAPCOUNT = 0x20000
    DDSCAPS_MIPMAP = 0x400000
    DDSCAPS_TEXTURE = 0x1000
    DDSCAPS_COMPLEX = 0x8

    stream.write(b'DDS ')
    write32(stream, 124) # DWORD dwSize;
    write32(stream, DDSD_CAPS | DDSD_HEIGHT | DDSD_WIDTH | DDSD_PIXELFORMAT | DDSD_MIPMAPCOUNT) # DWORD dwFlags;
    write32(stream, h) # DWORD dwHeight;
    write32(stream, w) # DWORD dwWidth;
    write32(stream, 0) # DWORD dwPitchOrLinearSize;
    write32(stream, 0) # DWORD dwDepth;
    write32(stream, len(mipmaps)) # DWORD dwMipMapCount;
    for _ in range(11):
        write32(stream, 0) # DWORD dwReserved1[11];

    if True:
        # Write DDS_PIXELFORMAT ddspf;
        DDPF_FOURCC = 0x4
        write32(stream, 32) # DWORD dwSize;
        write32(stream, DDPF_FOURCC) # DWORD dwFlags;
        stream.write(b'DX10') # DWORD dwFourCC;
        write32(stream, 0) # DWORD dwRGBBitCount;
        write32(stream, 0) # DWORD dwRBitMask;
        write32(stream, 0) # DWORD dwGBitMask;
        write32(stream, 0) # DWORD dwBBitMask;
        write32(stream, 0) # DWORD dwABitMask;

    write32(stream, DDSCAPS_TEXTURE | DDSCAPS_MIPMAP | DDSCAPS_COMPLEX) # DWORD dwCaps;
    write32(stream, 0) # DWORD dwCaps2;
    write32(stream, 0) # DWORD dwCaps3;
    write32(stream, 0) # DWORD dwCaps4;
    write32(stream, 0) # DWORD dwReserved2;

    # Write https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dds-header-dxt10

    # FIXME: put these in enum?
    D3D10_RESOURCE_DIMENSION_TEXTURE2D = 3
    DDS_ALPHA_MODE_STRAIGHT = 1

    write32(stream, ddsFormat[0]) # DXGI_FORMAT dxgiFormat;
    write32(stream, D3D10_RESOURCE_DIMENSION_TEXTURE2D) # D3D10_RESOURCE_DIMENSION resourceDimension;
    write32(stream, 0) # UINT miscFlag;
    write32(stream, 0) # UINT arraySize; #FIXME: Might be bad?
    write32(stream, DDS_ALPHA_MODE_STRAIGHT) # UINT miscFlags2;

    # DDS mipmap order is different from TGV
    for mipmap_file in mipmaps:
        stream.write(mipmap_file.getbuffer())

