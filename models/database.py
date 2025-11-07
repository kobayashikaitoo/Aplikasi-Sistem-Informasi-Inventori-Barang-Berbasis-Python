"""Lapisan akses database menggunakan SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

from utils.security import hash_password


class Database:
    """Kelas helper untuk koneksi dan inisialisasi database."""

    def __init__(self, db_path: str = "data/inventori.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """Membuat koneksi baru ke database."""

        conn = sqlite3.connect(self.db_path.as_posix())
        conn.row_factory = sqlite3.Row
        return conn

    def initialize(self) -> None:
        """Membuat tabel dan data awal jika belum tersedia."""

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.executescript(
            """
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                level TEXT NOT NULL CHECK(level IN ('admin', 'user'))
            );

            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_name TEXT NOT NULL,
                address TEXT
            );

            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_code TEXT UNIQUE NOT NULL,
                item_name TEXT NOT NULL,
                category_id INTEGER,
                stock INTEGER NOT NULL DEFAULT 0,
                purchase_price REAL DEFAULT 0,
                selling_price REAL DEFAULT 0,
                supplier_id INTEGER,
                FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE SET NULL,
                FOREIGN KEY(supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_date TEXT NOT NULL,
                item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                transaction_type TEXT NOT NULL CHECK(transaction_type IN ('IN', 'OUT')),
                notes TEXT,
                FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
            );
            """
        )

        self._ensure_default_records(cursor)
        conn.commit()
        conn.close()

    def _ensure_default_records(self, cursor: sqlite3.Cursor) -> None:
        """Menambahkan data awal seperti user admin dan kategori default."""

        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO users (username, password, level) VALUES (?, ?, ?)",
                ("admin", hash_password("admin123"), "admin"),
            )
            cursor.execute(
                "INSERT INTO users (username, password, level) VALUES (?, ?, ?)",
                ("staf", hash_password("staf123"), "user"),
            )

        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            categories: Iterable[str] = ["Sembako", "Minuman", "Perlengkapan", "Elektronik"]
            cursor.executemany(
                "INSERT INTO categories (name) VALUES (?)",
                [(name,) for name in categories],
            )

        cursor.execute("SELECT COUNT(*) FROM suppliers")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO suppliers (supplier_name, address) VALUES (?, ?)",
                [
                    ("PT Nusantara", "Jl. Raya 1"),
                    ("CV Sejahtera", "Jl. Mawar 5"),
                    ("UD Makmur", "Jl. Anggrek 9"),
                ],
            )

        cursor.execute("SELECT COUNT(*) FROM items")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                """
                INSERT INTO items (
                    item_code, item_name, category_id, stock, purchase_price, selling_price, supplier_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    ("BRG-001", "Beras 5kg", 1, 30, 55000, 65000, 1),
                    ("BRG-002", "Gula 1kg", 1, 40, 12000, 15000, 2),
                    ("BRG-003", "Minyak Goreng 1L", 2, 25, 14000, 17000, 2),
                    ("BRG-004", "Detergen 800gr", 3, 15, 18000, 23000, 3),
                    ("BRG-005", "Kabel USB", 4, 20, 10000, 15000, 1),
                ],
            )

        cursor.execute("SELECT COUNT(*) FROM transactions")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                """
                INSERT INTO transactions (transaction_date, item_id, quantity, transaction_type, notes)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    ("2025-11-01", 1, 10, "IN", "Restock awal"),
                    ("2025-11-02", 2, 5, "OUT", "Penjualan pelanggan"),
                    ("2025-11-03", 3, 8, "IN", "Pembelian supplier"),
                ],
            )

