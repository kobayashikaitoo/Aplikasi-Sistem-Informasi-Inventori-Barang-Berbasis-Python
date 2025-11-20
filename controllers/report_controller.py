"""Controller untuk pembuatan laporan."""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

class ReportController:
    def __init__(self, report_service: "ReportService") -> None:
        self.report_service = report_service

    def export_pdf(self, items: List[dict], transactions: List[dict], destination: str) -> Tuple[bool, str]:
        try:
            path = Path(destination)
            path.parent.mkdir(parents=True, exist_ok=True)
            self.report_service.generate_complete_pdf(items, transactions, path)
            return True, f"Laporan Lengkap PDF tersimpan di {path}"
        except Exception as exc:  # noqa: BLE001
            return False, f"Gagal membuat laporan PDF: {exc}"

    def export_excel(self, items: List[dict], transactions: List[dict], destination: str) -> Tuple[bool, str]:
        try:
            path = Path(destination)
            path.parent.mkdir(parents=True, exist_ok=True)
            self.report_service.generate_complete_excel(items, transactions, path)
            return True, f"Laporan Lengkap Excel tersimpan di {path}"
        except Exception as exc:  # noqa: BLE001
            return False, f"Gagal membuat laporan Excel: {exc}"


