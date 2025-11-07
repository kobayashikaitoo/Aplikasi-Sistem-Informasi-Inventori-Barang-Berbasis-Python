-- Skrip SQL untuk inisialisasi database Inventori
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    level TEXT NOT NULL CHECK(level IN ('admin','user'))
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT NOT NULL,
    address TEXT
);

CREATE TABLE items (
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

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_date TEXT NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    transaction_type TEXT NOT NULL CHECK(transaction_type IN ('IN','OUT')),
    notes TEXT,
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
);

INSERT INTO users (username, password, level) VALUES
('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin'),
('staf', 'd55ed37faf535e9b24d7baa04173735b9565d3421d4fb672b18f2730e27fc5c8', 'user');

INSERT INTO categories (name) VALUES
('Sembako'),
('Minuman'),
('Perlengkapan'),
('Elektronik'),
('Lainnya');

INSERT INTO suppliers (supplier_name, address) VALUES
('PT Nusantara', 'Jl. Raya 1'),
('CV Sejahtera', 'Jl. Mawar 5'),
('UD Makmur', 'Jl. Anggrek 9'),
('PT Sentosa', 'Jl. Melati 12'),
('CV Mandiri', 'Jl. Kenanga 3');

INSERT INTO items (item_code, item_name, category_id, stock, purchase_price, selling_price, supplier_id) VALUES
('BRG-001', 'Beras 5kg', 1, 30, 55000, 65000, 1),
('BRG-002', 'Gula 1kg', 1, 40, 12000, 15000, 2),
('BRG-003', 'Minyak Goreng 1L', 2, 25, 14000, 17000, 2),
('BRG-004', 'Detergen 800gr', 3, 15, 18000, 23000, 3),
('BRG-005', 'Kabel USB', 4, 20, 10000, 15000, 4),
('BRG-006', 'Sabun Mandi', 3, 18, 7000, 10000, 5),
('BRG-007', 'Air Mineral 600ml', 2, 50, 2500, 4000, 2),
('BRG-008', 'Lampu LED 12W', 4, 22, 18000, 25000, 4),
('BRG-009', 'Tepung Terigu 1kg', 1, 35, 9000, 12000, 1),
('BRG-010', 'Baterai AA', 4, 28, 6000, 9000, 3);

INSERT INTO transactions (transaction_date, item_id, quantity, transaction_type, notes) VALUES
('2025-11-01', 1, 10, 'IN', 'Restock awal'),
('2025-11-01', 2, 5, 'OUT', 'Penjualan toko'),
('2025-11-02', 3, 6, 'IN', 'Pembelian supplier'),
('2025-11-03', 4, 3, 'OUT', 'Penjualan pelanggan'),
('2025-11-03', 5, 12, 'IN', 'Restock gudang'),
('2025-11-04', 6, 4, 'OUT', 'Penjualan eceran'),
('2025-11-04', 7, 25, 'IN', 'Pengiriman supplier'),
('2025-11-05', 8, 5, 'OUT', 'Penjualan toko'),
('2025-11-05', 9, 8, 'IN', 'Restock toko'),
('2025-11-06', 10, 6, 'OUT', 'Penjualan grosir');

