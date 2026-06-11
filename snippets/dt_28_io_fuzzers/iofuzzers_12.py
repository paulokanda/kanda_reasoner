import struct
import random
from pathlib import Path

OUTPUT_DIR = Path("io_fuzzers_12/fuzzed_edf_samples")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_malformed_edf(filename):
    with open(OUTPUT_DIR / filename, "wb") as f:
        # Start with a mostly valid EDF header but introduce randomness
        header = bytearray(256)
        header[:8] = b"0       "  # version
        header[8:88] = b"FuzzedPatient                          " * 2  # patient & recording
        header[88:96] = b"01.01.01"  # date
        header[96:104] = b"01.01.01"  # time
        header[184:192] = f"{random.randint(0, 99999999):08}".encode("ascii")  # header bytes
        header[252:256] = b"1   "  # one signal
        f.write(header)

        # Now inject malformed data
        for _ in range(1000):
            value = random.randint(-32768, 32767)
            if random.random() < 0.05:
                # corrupt byte
                f.write(b"\xFF\xFF")
            else:
                f.write(struct.pack("<h", value))

def main():
    for i in range(5):
        generate_malformed_edf(f"fuzzed_sample_{i}.edf")
    print(f"✅ Fuzzed EDF files written to {OUTPUT_DIR.resolve()}")

if __name__ == "__main__":
    main()