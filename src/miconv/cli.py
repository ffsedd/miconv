import argparse
from pathlib import Path

from .registry import available, get, load_converters


def infer_output(src: Path) -> Path:
    return src.with_suffix(".xlsx")


def main() -> None:
    load_converters()
    parser = argparse.ArgumentParser()
    parser.add_argument("converter", choices=available())
    parser.add_argument("src")
    parser.add_argument("dst", nargs="?")  # optional

    args = parser.parse_args()

    src = Path(args.src)
    dst = Path(args.dst) if args.dst else infer_output(src)

    conv_cls = get(args.converter)
    conv = conv_cls()

    conv.run(src, dst)
