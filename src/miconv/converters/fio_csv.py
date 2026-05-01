from pathlib import Path
import pandas as pd

from ..base import Converter
from ..registry import register


@register
class FioCSV(Converter):
    name = "fio"

    def read(self, path: Path) -> pd.DataFrame:
        return pd.read_csv(
            path,
            sep=";",
            dtype=str,
            encoding="utf-8",
        )

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")
        df["Objem"] = df["Objem"].str.replace(",", ".").astype(float)
        return df

    def write(self, df: pd.DataFrame, path: Path) -> None:
        df.to_excel(path, index=False)
