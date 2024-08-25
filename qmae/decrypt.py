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
            0xD693674AC3DCB8CED1147FFACF9DE69EA0E1C351B230EC95C8C0F2DE73324877,
            0xF740845E6CF6B591F492C767B63EAEEBE0A26F7E906108F0A4A28DCA7091C228,
            0x957C6A47D8264A922CFFB5848B41A66843AD1152CC25F4288941ABD57F021BF3,
            0x66FC8BC606A2D84116A29AAADC177308CCAFD9A175C3758958473FBBCBE6CC61,
            0x74AC43F3B388C908C29C6562BCA78CE637AFE99270272BE7740AA02318CF9F34,
            0x3F1BF31D11EFA84FE8406DA06AD6397A957835F49F484E956401C3A1AFD40F2C,
            0x0968ED0E601940F1A4BD1A134753FE4916CD0EF0370EEFFB1930195B6FDD073F,
            0x114A7900F6F747A56C0CFDBC00DB711C762BA4F9DAD9E47720FE1A3DCF4D5F06,
        ]:
            self._table += block.to_bytes(32, byteorder="little")

    def decrypt(self, data: Union[bytes, bytearray, np.ndarray]) -> bytes:

        for idx in range(len(data)):
            data[idx] ^= self._table[(idx * idx + 27) % len(self._table)]

        return data
