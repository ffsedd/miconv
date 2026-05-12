from __future__ import annotations

from pathlib import Path
import pandas as pd

from ..base import Converter
from ..registry import register


REQUIRED_COLUMNS = {
    "Datum splatnosti",
    "Částka",
}


# -----------------------------------------------------
# helpers
# -----------------------------------------------------

def find_header_row(path: Path) -> int:
    """Locate table header inside KB export."""
    with path.open("r", encoding="cp1250", errors="ignore") as f:
        for i, line in enumerate(f):
            if "Datum splatnosti" in line:
                return i
    raise ValueError("KB CSV header not found")


def parse_cz_float(s: pd.Series) -> pd.Series:
    """Parse Czech formatted signed numbers."""
    return (
        s.fillna("")
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
        .replace("", pd.NA)
        .astype("Float64")
    )


# -----------------------------------------------------
# converter
# -----------------------------------------------------

@register
class KBCSV(Converter):
    name = "kb"
        
    @classmethod
    def sniff(cls, path: Path) -> bool:
        with path.open("r", encoding="cp1250", errors="ignore") as f:
            head = f.read(500)

        return "MojeBanka" in head

    # ---------------- READ ----------------

    def read(self, path: Path) -> pd.DataFrame:
        header_row = find_header_row(path)

        df = pd.read_csv(
            path,
            sep=";",
            encoding="cp1250",  # KB encoding
            dtype=str,
            skiprows=header_row,
        )

        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"Missing KB columns: {missing}")

        return df

    # ---------------- TRANSFORM ----------------

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()

        # date
        out["Datum splatnosti"] = pd.to_datetime(
            out["Datum splatnosti"],
            format="%d.%m.%Y",
            errors="raise",
        )

        # amount
        out["Částka"] = parse_cz_float(out["Částka"])

        return out

    # ---------------- WRITE ----------------

    def write(self, df: pd.DataFrame, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(path, index=False)
