"""Validator sederhana untuk memeriksa kelengkapan data form."""

from typing import Dict, Tuple


def validate_required_fields(data: Dict[str, str]) -> Tuple[bool, str]:
    """Periksa apakah semua field yang diwajibkan terisi."""

    missing = [label for label, value in data.items() if value in ("", None)]
    if missing:
        return False, f"Field berikut wajib diisi: {', '.join(missing)}"
    return True, "Data valid"

