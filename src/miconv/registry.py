from pathlib import Path

_REGISTRY = {}


def register(cls):
    _REGISTRY[cls.name] = cls
    return cls


def get(name: str):
    return _REGISTRY[name]


def load_converters():
    import miconv.converters as pkg
    import pkgutil
    import importlib

    for m in pkgutil.iter_modules(pkg.__path__):
        importlib.import_module(f"{pkg.__name__}.{m.name}")


def detect(path: Path):
    load_converters()

    for cls in _REGISTRY.values():
        if hasattr(cls, "sniff") and cls.sniff(path):
            return cls()

    raise ValueError(f"Format Detect failed: {path}")
