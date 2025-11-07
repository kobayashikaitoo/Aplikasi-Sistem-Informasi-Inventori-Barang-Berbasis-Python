"""Builder chart menggunakan matplotlib untuk ditampilkan di Tkinter."""

from typing import Iterable, Mapping

from matplotlib.figure import Figure


class ChartBuilder:
    """Menyediakan utilitas untuk membuat grafik stok barang."""

    def __init__(self) -> None:
        self.figure = Figure(figsize=(5, 3), dpi=100)

    def build_stock_chart(self, items: Iterable[Mapping[str, object]]) -> Figure:
        """Bangun grafik batang sederhana berdasarkan stok barang."""

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        names = [item["item_name"] for item in items]
        stocks = [item["stock"] for item in items]

        ax.bar(names, stocks, color="#3f72af")
        ax.set_title("Grafik Stok Barang")
        ax.set_ylabel("Jumlah Stok")
        ax.set_xlabel("Barang")
        ax.tick_params(axis="x", rotation=45, labelsize=8)
        ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)
        self.figure.tight_layout()
        return self.figure

