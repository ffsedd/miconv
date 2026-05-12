from pathlib import Path
import sys

from .registry import detect


def main():
    if len(sys.argv) == 3:
        src = Path(sys.argv[1])
        dst = Path(sys.argv[2])

    elif len(sys.argv) == 2:
        src = Path(sys.argv[1])
        dst = src.with_suffix(".xlsx")

    else:
        print("Usage: miconv <input> [output]")
        sys.exit(2)

    converter = detect(src)
    df = converter.convert(src)
    df.to_excel(dst, index=False)
