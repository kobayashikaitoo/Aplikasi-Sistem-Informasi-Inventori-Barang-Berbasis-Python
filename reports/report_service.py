"""Service pembuatan laporan PDF dan Excel."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable, Mapping

from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


class ReportService:
    """Menyediakan utilitas untuk mengekspor laporan stok barang."""

    def generate_pdf(self, items: Iterable[Mapping[str, object]], destination: Path) -> None:
        pdf = canvas.Canvas(destination.as_posix(), pagesize=A4)
        width, height = A4
        pdf.setTitle("Laporan Stok Barang")

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(2 * cm, height - 2 * cm, "Laporan Stok Barang")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(2 * cm, height - 2.7 * cm, f"Tanggal Cetak: {datetime.now():%d-%m-%Y %H:%M}")

        table_top = height - 3.5 * cm
        col_widths = [3 * cm, 5 * cm, 2 * cm, 3 * cm, 3 * cm]
        headers = ["Kode", "Nama", "Stok", "Harga Beli", "Harga Jual"]

        pdf.setFillColor(colors.lightgrey)
        pdf.rect(2 * cm, table_top, sum(col_widths), 0.7 * cm, fill=1, stroke=0)
        pdf.setFillColor(colors.black)

        x = 2 * cm
        for idx, header in enumerate(headers):
            pdf.drawString(x + 0.2 * cm, table_top + 0.2 * cm, header)
            x += col_widths[idx]

        y = table_top - 0.5 * cm
        for item in items:
            if y < 3 * cm:
                pdf.showPage()
                y = height - 3 * cm
            pdf.drawString(2.2 * cm, y, str(item["item_code"]))
            pdf.drawString(5.2 * cm, y, str(item["item_name"]))
            pdf.drawRightString(2 * cm + col_widths[0] + col_widths[1] + 1.8 * cm, y, str(item["stock"]))
            pdf.drawRightString(2 * cm + sum(col_widths[:4]) - 0.2 * cm, y, f"{item['purchase_price']:.0f}")
            pdf.drawRightString(2 * cm + sum(col_widths) - 0.2 * cm, y, f"{item['selling_price']:.0f}")
            y -= 0.5 * cm

        pdf.showPage()
        pdf.save()

    def generate_excel(self, items: Iterable[Mapping[str, object]], destination: Path) -> None:
        wb = Workbook()
        ws = wb.active
        ws.title = "Stok Barang"
        ws.append(["Kode", "Nama", "Kategori", "Stok", "Harga Beli", "Harga Jual", "Pemasok"])

        for item in items:
            ws.append(
                [
                    item["item_code"],
                    item["item_name"],
                    item.get("category", "-"),
                    item["stock"],
                    item["purchase_price"],
                    item["selling_price"],
                    item.get("supplier", "-"),
                ]
            )

        for column_cells in ws.columns:
            length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
            ws.column_dimensions[column_cells[0].column_letter].width = length + 2

        wb.save(destination.as_posix())

