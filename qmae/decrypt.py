from typing import Union
import warnings

import numpy as np


def read_encfile(filename: str) -> tuple:

    toint = lambda x: int.from_bytes(x, byteorder="big")

    with open(filename, "rb") as fin:

        magic = fin.read(4)
        assert magic == b"QMAE"

        ldata = toint(fin.read(4))
        fin.read(8)  # unused

        lkey = toint(fin.read(1)) - 1
        assert lkey % 4 == 0
        key0 = bytearray(fin.read(lkey + 1))
        key = np.array(key0[:4] + key0[5:]) ^ key0[4]

        data = bytearray(fin.read(ldata))

    return key, data


class QMAEDecryptor:

    def __init__(self):
        # makes key table; could have hardcoded a 256-element array,
        # but black formatter doesn't like putting multiple elements in a single line

        self._table = bytearray()
        for block in [
            0xC34AD6CA_9067F752_D8A16662_9F5B0900,
            0xC35E9523_9F13117E_D8923FBC_90BB740E,
            0xC347743D_90AA3F51_D8F41184_9FDE951D,
            0xC3C609D5_9FFA66F9_D8F0F7A0_90A1D6F3,
            0xC3F3D6A1_90A0F7F0_D8F966FA_9FD509C6,
            0xC31D95DE_9F8411F4_D8513FAA_903D7447,
            0xC30E74BB_90BC3F92_D87E1113_9F23955E,
            0xC300095B_9F6266A1_D852F767_90CAD64A,
        ]:
            self._table += block.to_bytes(16, byteorder="big")

    def decrypt(self, data: Union[bytes, bytearray, np.ndarray]) -> bytes:

        for idx in range(len(data)):
            data[idx] ^= self._table[idx % len(self._table)]

        return data
