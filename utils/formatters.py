"""Formatter utilitas untuk menampilkan angka dan teks."""


def format_currency(value: float) -> str:
    """Format nilai float menjadi bentuk mata uang sederhana."""

    try:
        value_str = f"{value:,.2f}"
        integer_part, decimal_part = value_str.split(".")
        integer_part = integer_part.replace(",", ".")
        return f"Rp {integer_part},{decimal_part}"
    except (TypeError, ValueError):
        return "Rp 0,00"

