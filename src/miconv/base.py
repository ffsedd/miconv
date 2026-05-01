from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd


class Converter(ABC):
    name: str

    @abstractmethod
    def read(self, path: Path) -> pd.DataFrame:
        ...

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        ...

    @abstractmethod
    def write(self, df: pd.DataFrame, path: Path) -> None:
        ...

    def run(self, src: Path, dst: Path) -> None:
        df = self.read(src)
        df = self.transform(df)
        self.write(df, dst)
