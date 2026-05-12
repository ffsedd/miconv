from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd


CANONICAL_COLUMNS = []  # optional now


class Converter(ABC):
    name: str

    @classmethod
    @abstractmethod
    def sniff(cls, path: Path) -> bool:
        ...

    @abstractmethod
    def read(self, path: Path) -> pd.DataFrame:
        ...

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add normalized columns but DO NOT drop original ones.
        """

    def convert(self, path: Path) -> pd.DataFrame:
        df = self.read(path)
        df = self.transform(df)

        # optional validation only (not blocking)
        missing = set(CANONICAL_COLUMNS) - set(df.columns)
        if missing:
            raise ValueError(f"{self.name}: missing required columns {missing}")

        return df
