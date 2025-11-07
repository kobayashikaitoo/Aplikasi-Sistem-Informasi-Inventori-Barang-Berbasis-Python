"""Model transaksi sederhana untuk stock in/out."""

from __future__ import annotations

from typing import Dict, List


class TransactionModel:
    def __init__(self, database: "Database") -> None:
        self.database = database

    def add_transaction(self, data: Dict[str, object]) -> None:
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (transaction_date, item_id, quantity, transaction_type, notes) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                data["transaction_date"],
                data["item_id"],
                data["quantity"],
                data["transaction_type"],
                data.get("notes"),
            ),
        )

        if data["transaction_type"] == "IN":
            cursor.execute(
                "UPDATE items SET stock = stock + ? WHERE id = ?",
                (data["quantity"], data["item_id"]),
            )
        else:
            cursor.execute(
                "UPDATE items SET stock = stock - ? WHERE id = ?",
                (data["quantity"], data["item_id"]),
            )

        conn.commit()
        conn.close()

    def get_recent(self, limit: int = 10) -> List[dict]:
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT transactions.id, transaction_date, transaction_type, quantity, item_name
            FROM transactions
            JOIN items ON items.id = transactions.item_id
            ORDER BY transaction_date DESC, transactions.id DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_all(self) -> List[dict]:
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT transactions.id, transaction_date, transaction_type, quantity, notes,
                   items.item_name
            FROM transactions
            JOIN items ON items.id = transactions.item_id
            ORDER BY transaction_date DESC
            """
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

