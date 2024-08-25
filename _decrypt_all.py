import os

from qmae.decrypt import QMAEDecryptor

# Unlike audioeffect-ncm, we circumvent QMAEScheme
# and directly use QMAEDecryptor since
#   (1) read_encfile is deprecated here since the key is hardcoded,
#       so all encrypted files are treated as unstructured raw binary, and
#   (2) the structure of QMAEScheme remains unclear
#       at the point the decryption function is written.


dsrc = "resae"
ddst = "processed"


exceptions = [
    os.path.join("recommend", "SleepEffect"),
    os.path.join("DJRemix"),
    os.path.join("ugc", "DJ"),
]


if __name__ == "__main__":

    decryptor = QMAEDecryptor()
    # use common decryptor since key is hardcoded

    for r, d, f in os.walk(dsrc):
        for a in f:
            p = os.path.join(r, a)
            p_new = p.replace(dsrc, ddst)
            base, ext = os.path.splitext(p_new)

            # ignored folders
            skip = False
            for e in exceptions:
                if p.startswith(os.path.join(dsrc, e)):
                    skip = True
                    break
            if skip:
                continue

            # ignored extensions
            if ext in [".json", ".csv"]:
                continue

            # make directory at destination when necessary
            os.makedirs(os.path.dirname(p_new), exist_ok=True)

            with open(p, "rb") as fin:
                data = bytearray(fin.read())

            # waived extensions
            if ext in [".aep", ".wav"]:
                with open(p_new, "wb") as fout:
                    fout.write(data)  # why isn't there an os.copy()?
                    continue

            data_dec = decryptor.decrypt(data)

            if data_dec.startswith(b"RIFF"):
                p_new = base + ".wav"

            if ext == ".qmaep":
                p_new = base + ".aep"

            with open(p_new, "wb") as fout:
                fout.write(data_dec)

            print(p)
