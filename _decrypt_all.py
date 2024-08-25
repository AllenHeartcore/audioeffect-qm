import warnings

import os
import json

from qmae.scheme import QMAEScheme


dsrc = "presets"
ddst = "data/processed"


if __name__ == "__main__":

    warnings.filterwarnings("ignore", category=UserWarning)
    # otherwise, scheme.export() always warns about file extension mismatch (.bin)

    with open("_translate.json", encoding="utf-8") as f:
        translator = json.load(f)

    for src, dst in translator.items():
        scheme = QMAEScheme(os.path.join(dsrc, src) + ".qmae")
        scheme.export(
            os.path.join(ddst, dst) + ".bin", fmt="/" in dst
        )  # device-specific presets
        print(src, "->", dst)
