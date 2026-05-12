from pathlib import Path


FIO_CSV = """Datum;Objem;Měna;Protiúčet;Kód banky;Zpráva pro příjemce;Poznámka;VS;Název protiúčtu;Zadal;SS;Typ;Reference plátce
01.01.2025;-1500;CZK;XXXXXXXXXX;5500;internal allowance transfer;internal allowance transfer;;;"";"";Bezhotovostní platba;
06.01.2025;-1800;CZK;XXXXXXXXXXXX;6210;activity fee;activity fee;;;"";"";Bezhotovostní platba;
07.01.2025;-5000;CZK;XXXXXXXXXX;2010;household expenses weekly budget;household expenses weekly budget;;budget-category-01;;;Platba převodem uvnitř banky;
10.01.2025;5000;CZK;XXXXXXXXXX;2010;internal transfer income;internal transfer income;;salary-like-transfer;;;Platba převodem uvnitř banky;
"""


def test_fio(tmp_path):
    from miconv.registry import get, load_converters

    load_converters()

    src = tmp_path / "fio.csv"
    src.write_text(FIO_CSV, encoding="utf-8")

    out = tmp_path / "out.xlsx"

    conv = get("fio")()
    conv.run(src, out)

    assert out.exists()
