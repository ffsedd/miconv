def parse_cz_float(s: str | None) -> float | None:
    if not s:
        return None
    return float(s.replace(",", "."))
