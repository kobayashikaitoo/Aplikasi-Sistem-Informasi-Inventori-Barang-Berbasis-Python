"""Controller untuk operasi pemasok."""

from __future__ import annotations

from typing import Dict, List, Tuple

from utils.validators import validate_required_fields

class SupplierController:
    def __init__(self, supplier_model: "SupplierModel") -> None:
        self.supplier_model = supplier_model

    def list_suppliers(self, keyword: str = "") -> List[dict]:
        return self.supplier_model.get_all(keyword)

    def add_supplier(self, data: Dict[str, str]) -> Tuple[bool, str]:
        valid, message = validate_required_fields({"Nama Pemasok": data.get("supplier_name")})
        if not valid:
            return False, message
        try:
            self.supplier_model.create(data)
            return True, "Pemasok berhasil ditambahkan"
        except Exception as exc:  # noqa: BLE001
            return False, f"Gagal menambahkan pemasok: {exc}"

    def update_supplier(self, supplier_id: int, data: Dict[str, str]) -> Tuple[bool, str]:
        valid, message = validate_required_fields({"Nama Pemasok": data.get("supplier_name")})
        if not valid:
            return False, message
        try:
            self.supplier_model.update(supplier_id, data)
            return True, "Pemasok berhasil diperbarui"
        except Exception as exc:  # noqa: BLE001
            return False, f"Gagal memperbarui pemasok: {exc}"

    def delete_supplier(self, supplier_id: int) -> Tuple[bool, str]:
        try:
            self.supplier_model.delete(supplier_id)
            return True, "Pemasok berhasil dihapus"
        except Exception as exc:  # noqa: BLE001
            return False, f"Gagal menghapus pemasok: {exc}"

