from __future__ import annotations

from typing import Dict, Type

from .base import Converter

_REGISTRY: Dict[str, Type[Converter]] = {}


def load_converters() -> None:
    from .converters import fio_csv  # noqa


def register(cls: Type[Converter]) -> Type[Converter]:
    _REGISTRY[cls.name] = cls
    return cls


def get(name: str) -> Type[Converter]:
    return _REGISTRY[name]


def available() -> list[str]:
    return sorted(_REGISTRY)
