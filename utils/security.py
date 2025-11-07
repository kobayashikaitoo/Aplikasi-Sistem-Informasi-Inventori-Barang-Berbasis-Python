"""Fungsi keamanan sederhana untuk hashing password."""

import hashlib


def hash_password(password: str) -> str:
    """Menghasilkan hash SHA-256 dari password."""

    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Memverifikasi kecocokan password dengan hash."""

    return hash_password(password) == hashed

