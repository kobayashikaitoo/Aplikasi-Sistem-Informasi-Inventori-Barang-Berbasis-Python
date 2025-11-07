"""Model untuk data pemasok."""

from __future__ import annotations

from typing import Dict, List, Optional


class SupplierModel:
    def __init__(self, database: "Database") -> None:
        self.database = database

    def get_all(self, keyword: str = "") -> List[dict]:
        conn = self.database.get_connection()
        cursor = conn.cursor()
        query = "SELECT id, supplier_name, address FROM suppliers"
        params = []
        if keyword:
            query += " WHERE supplier_name LIKE ? OR IFNULL(address, '') LIKE ?"
            like = f"%{keyword}%"
            params = [like, like]
        query += " ORDER BY supplier_name"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_by_id(self, supplier_id: int) -> Optional[dict]:
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, supplier_name, address FROM suppliers WHERE id = ?",
            (supplier_id,),
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def create(self, data: Dict[str, str]) -> None:
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO suppliers (supplier_name, address) VALUES (?, ?)",
            (data["supplier_name"], data.get("address")),
        )
        conn.commit()
        conn.close()

    def update(self, supplier_id: int, data: Dict[str, str]) -> None:
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE suppliers SET supplier_name = ?, address = ? WHERE id = ?",
            (data["supplier_name"], data.get("address"), supplier_id),
        )
        conn.commit()
        conn.close()

    def delete(self, supplier_id: int) -> None:
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM suppliers WHERE id = ?", (supplier_id,))
        conn.commit()
        conn.close()

