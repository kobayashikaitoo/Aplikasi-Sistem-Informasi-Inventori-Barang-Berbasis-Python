"""Model untuk mengelola data pengguna."""

from __future__ import annotations

from typing import List, Optional

from utils.security import hash_password, verify_password


class UserModel:
    """Menyediakan operasi CRUD untuk tabel users."""

    def __init__(self, database: "Database") -> None:
        self.database = database

    def authenticate(self, username: str, password: str) -> Optional[dict]:
        """Validasi kredensial pengguna."""

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password, level FROM users WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()
        conn.close()

        if row and verify_password(password, row["password"]):
            return {
                "id": row["id"],
                "username": row["username"],
                "level": row["level"],
            }
        return None

    def get_all(self) -> List[dict]:
        """Ambil seluruh data pengguna."""

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, level FROM users ORDER BY username")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def create_user(self, username: str, password: str, level: str) -> None:
        """Tambahkan user baru."""

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, level) VALUES (?, ?, ?)",
            (username, hash_password(password), level),
        )
        conn.commit()
        conn.close()

    def update_user(self, user_id: int, level: str) -> None:
        """Perbarui level user."""

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET level = ? WHERE id = ?",
            (level, user_id),
        )
        conn.commit()
        conn.close()

    def change_password(self, user_id: int, new_password: str) -> None:
        """Ganti password user."""

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (hash_password(new_password), user_id),
        )
        conn.commit()
        conn.close()

    def delete_user(self, user_id: int) -> None:
        """Hapus user."""

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

