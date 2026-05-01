from pathlib import Path

DATA = Path(__file__).parent / "data"


def test_fio(tmp_path):
    from miconv.registry import get, load_converters

    load_converters()

    conv = get("fio")()
    out = tmp_path / "out.xlsx"

    conv.run(DATA / "fio_input.csv", out)

    assert out.exists()
