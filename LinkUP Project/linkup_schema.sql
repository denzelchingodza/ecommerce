-- ============================================================
--  LinkUP — MySQL Database Schema
--  This defines the tables a real PHP/MySQL backend would use.
--  Each table mirrors a localStorage key in the demo app.
-- ============================================================

CREATE DATABASE IF NOT EXISTS linkup_db;
USE linkup_db;

-- ── USERS ────────────────────────────────────────────────────
-- Mirrors: localStorage key 'linkup_users'
-- Stores all registered accounts.
-- is_banned: admin sets to 1 to block login immediately.

CREATE TABLE users (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100)  NOT NULL,
    email      VARCHAR(150)  NOT NULL UNIQUE,
    password   VARCHAR(255)  NOT NULL,         -- bcrypt hashed
    is_banned  TINYINT(1)    DEFAULT 0,
    created_at DATETIME      DEFAULT NOW()
);


-- ── PRODUCTS ─────────────────────────────────────────────────
-- Mirrors: localStorage key 'admin_products'
-- Stores all seller listings.
-- status: 'active' shows on marketplace, 'suspended' is hidden.

CREATE TABLE products (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    title             VARCHAR(200)   NOT NULL,
    price             DECIMAL(10,2)  NOT NULL,
    category          VARCHAR(100),
    product_condition VARCHAR(50),               -- New / Used / Refurbished
    description       TEXT,
    seller_email      VARCHAR(150),
    image_url         VARCHAR(500),
    status            ENUM('active','suspended') DEFAULT 'active',
    created_at        DATETIME DEFAULT NOW(),
    FOREIGN KEY (seller_email) REFERENCES users(email)
);


-- ── ORDERS ───────────────────────────────────────────────────
-- Mirrors: localStorage key 'linkup_orders'
-- Saves confirmed orders after PayFast or COD checkout.

CREATE TABLE orders (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    buyer_email    VARCHAR(150),
    items_json     TEXT,                          -- cart items as JSON
    total          DECIMAL(10,2),
    payment_method ENUM('PayFast','COD') DEFAULT 'COD',
    status         VARCHAR(50)          DEFAULT 'confirmed',
    created_at     DATETIME DEFAULT NOW(),
    FOREIGN KEY (buyer_email) REFERENCES users(email)
);


-- ── SAVED ITEMS (WISHLIST) ───────────────────────────────────
-- Mirrors: localStorage key 'linkup_saved'
-- Products a buyer saved to their wishlist.

CREATE TABLE saved_items (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_email   VARCHAR(150),
    product_id   INT,
    saved_at     DATETIME DEFAULT NOW(),
    FOREIGN KEY (user_email)  REFERENCES users(id),
    FOREIGN KEY (product_id)  REFERENCES products(id)
);


-- ── SAMPLE DATA (for demo / testing) ────────────────────────

INSERT INTO users (name, email, password, is_banned) VALUES
('Admin',          'admin@linkup.com',        '$2y$10$examplehashedpassword1', 0),
('Denzel Chingodza','denzel@example.com',     '$2y$10$examplehashedpassword2', 0),
('Demo Seller',    'seller@example.com',      '$2y$10$examplehashedpassword3', 0);

INSERT INTO products (title, price, category, product_condition, description, seller_email, status) VALUES
('iPhone 13 Pro',   12500.00, 'Electronics', 'Used',        'Great condition, minor scratches.', 'seller@example.com', 'active'),
('Nike Air Max',     850.00, 'Clothing',     'New',          'Size 10, never worn.',             'seller@example.com', 'active'),
('Study Desk',       450.00, 'Furniture',    'Used',         'Solid wood, fits small room.',     'denzel@example.com', 'active'),
('Suspicious Item',   10.00, 'Other',        'Refurbished',  'This listing was flagged.',        'seller@example.com', 'suspended');
