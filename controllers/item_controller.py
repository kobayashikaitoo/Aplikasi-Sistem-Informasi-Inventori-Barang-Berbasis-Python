"""Controller untuk mengelola barang dan transaksi stok."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Tuple

from utils.validators import validate_required_fields


class ItemController:
    def __init__(self, item_model: "ItemModel", transaction_model: "TransactionModel") -> None:
        self.item_model = item_model
        self.transaction_model = transaction_model

    def list_items(self, keyword: str = "") -> List[dict]:
        return self.item_model.get_all(keyword)

    def get_categories(self) -> List[dict]:
        return self.item_model.get_categories()

    def add_item(self, data: Dict[str, object]) -> Tuple[bool, str]:
        required = {
            "Kode Barang": data.get("item_code"),
            "Nama Barang": data.get("item_name"),
        }
        valid, message = validate_required_fields(required)
        if not valid:
            return False, message
        try:
            self.item_model.create(data)
            return True, "Barang berhasil ditambahkan"
        except Exception as exc:  # noqa: BLE001
            return False, f"Gagal menambahkan barang: {exc}"

    def update_item(self, item_id: int, data: Dict[str, object]) -> Tuple[bool, str]:
        required = {
            "Kode Barang": data.get("item_code"),
            "Nama Barang": data.get("item_name"),
        }
        valid, message = validate_required_fields(required)
        if not valid:
            return False, message
        try:
            self.item_model.update(item_id, data)
            return True, "Barang berhasil diperbarui"
        except Exception as exc:  # noqa: BLE001
            return False, f"Gagal memperbarui barang: {exc}"

    def delete_item(self, item_id: int) -> Tuple[bool, str]:
        try:
            self.item_model.delete(item_id)
            return True, "Barang berhasil dihapus"
        except Exception as exc:  # noqa: BLE001
            return False, f"Gagal menghapus barang: {exc}"

    def record_transaction(self, data: Dict[str, object]) -> Tuple[bool, str]:
        required = {
            "Tanggal": data.get("transaction_date"),
            "Barang": data.get("item_id"),
            "Jumlah": data.get("quantity"),
            "Jenis": data.get("transaction_type"),
        }
        valid, message = validate_required_fields(required)
        if not valid:
            return False, message

        if isinstance(data.get("transaction_date"), datetime):
            data["transaction_date"] = data["transaction_date"].strftime("%Y-%m-%d")

        try:
            if data["transaction_type"] == "OUT":
                item = self.item_model.get_by_id(int(data["item_id"]))
                if item and item["stock"] < int(data["quantity"]):
                    return False, "Stok tidak mencukupi"
            self.transaction_model.add_transaction(data)
            return True, "Transaksi berhasil disimpan"
        except Exception as exc:  # noqa: BLE001
            return False, f"Gagal menyimpan transaksi: {exc}"

    def get_recent_transactions(self, limit: int = 10) -> List[dict]:
        return self.transaction_model.get_recent(limit)

    def get_all_transactions(self) -> List[dict]:
        return self.transaction_model.get_all()

