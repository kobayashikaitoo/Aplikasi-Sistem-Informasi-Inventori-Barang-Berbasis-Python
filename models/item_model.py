"""Model untuk operasi data barang."""

from __future__ import annotations

from typing import Dict, List, Optional


class ItemModel:
    """Mengelola tabel items."""

    def __init__(self, database: "Database") -> None:
        self.database = database

    def get_all(self, keyword: str = "") -> List[dict]:
        """Ambil semua barang dengan opsi pencarian."""

        conn = self.database.get_connection()
        cursor = conn.cursor()
        query = (
            "SELECT items.id, item_code, item_name, stock, purchase_price, selling_price, "
            "IFNULL(categories.name, '-') AS category, IFNULL(suppliers.supplier_name, '-') AS supplier "
            "FROM items "
            "LEFT JOIN categories ON categories.id = items.category_id "
            "LEFT JOIN suppliers ON suppliers.id = items.supplier_id "
        )
        params = []
        if keyword:
            query += (
                "WHERE item_code LIKE ? OR item_name LIKE ? OR IFNULL(categories.name, '') LIKE ? "
            )
            like = f"%{keyword}%"
            params = [like, like, like]
        query += "ORDER BY item_name"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_by_id(self, item_id: int) -> Optional[dict]:
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM items WHERE id = ?",
            (item_id,),
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def create(self, data: Dict[str, object]) -> None:
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO items (item_code, item_name, category_id, stock, purchase_price, selling_price, supplier_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["item_code"],
                data["item_name"],
                data.get("category_id"),
                data.get("stock", 0),
                data.get("purchase_price", 0.0),
                data.get("selling_price", 0.0),
                data.get("supplier_id"),
            ),
        )
        conn.commit()
        conn.close()

    def update(self, item_id: int, data: Dict[str, object]) -> None:
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE items
            SET item_code = ?, item_name = ?, category_id = ?, stock = ?, purchase_price = ?, selling_price = ?, supplier_id = ?
            WHERE id = ?
            """,
            (
                data["item_code"],
                data["item_name"],
                data.get("category_id"),
                data.get("stock", 0),
                data.get("purchase_price", 0.0),
                data.get("selling_price", 0.0),
                data.get("supplier_id"),
                item_id,
            ),
        )
        conn.commit()
        conn.close()

    def delete(self, item_id: int) -> None:
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()

    def adjust_stock(self, item_id: int, quantity: int, transaction_type: str) -> None:
        conn = self.database.get_connection()
        cursor = conn.cursor()
        if transaction_type == "IN":
            cursor.execute("UPDATE items SET stock = stock + ? WHERE id = ?", (quantity, item_id))
        else:
            cursor.execute("UPDATE items SET stock = stock - ? WHERE id = ?", (quantity, item_id))
        conn.commit()
        conn.close()

    def get_stock_summary(self) -> dict:
        """Ringkasan stok untuk dashboard."""

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total_barang, SUM(stock) AS total_stok FROM items")
        summary = cursor.fetchone()
        cursor.execute(
            "SELECT item_name, stock FROM items ORDER BY stock ASC LIMIT 5"
        )
        low_stock = cursor.fetchall()
        conn.close()
        return {
            "total_items": summary["total_barang"] if summary else 0,
            "total_stock": summary["total_stok"] if summary else 0,
            "low_stock_items": [dict(row) for row in low_stock],
        }

    def get_categories(self) -> List[dict]:
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

