from pathlib import Path
import pandas as pd


KB_SAMPLE = """\
"MojeBanka, export transakční historie";
"Datum vytvoření souboru";"12.05.2026";

"Datum splatnosti";"Datum odepsání z jiné banky";"Protiúčet a kód banky";"Název protiúčtu";"Částka";
"11.05.2026";"11.05.2026";"191918358/0600";"SOUCEK LUDVIK";"+3379,00";
"01.05.2026";;"";;"-15000,00";
"""


def test_kb(tmp_path):
    from miconv.registry import get, load_converters

    load_converters()

    src = tmp_path / "kb_input.csv"
    src.write_text(KB_SAMPLE, encoding="cp1250")

    conv = get("kb")()
    out = tmp_path / "out.xlsx"

    conv.run(src, out)

    assert out.exists()

    df = pd.read_excel(out)

    assert len(df) == 2
    assert df["Částka"].iloc[0] == 3379.0
    assert df["Částka"].iloc[1] == -15000.0
