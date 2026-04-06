-- =============================================================
-- BullLens Smart Stock Tracker – Database Schema
-- Run this file in MySQL to initialize the database
-- =============================================================

-- Create and select the database
CREATE DATABASE IF NOT EXISTS bulllens_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE bulllens_db;

-- -------------------------------------------------------------
-- Table: users
-- Stores registered user accounts
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id     INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    email       VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Demo user is auto-provisioned with bcrypt hash on app startup
-- Username: demo, Password: demo1234

-- -------------------------------------------------------------
-- Table: stocks
-- Master list of tracked stock symbols
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS stocks (
    stock_id     INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    symbol       VARCHAR(30)  NOT NULL UNIQUE,
    company_name VARCHAR(150) NOT NULL,
    exchange     VARCHAR(30)  DEFAULT 'NSE',
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- -------------------------------------------------------------
-- Table: watchlist
-- Maps users to stocks they are watching
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS watchlist (
    watchlist_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id      INT UNSIGNED NOT NULL,
    stock_id     INT UNSIGNED NOT NULL,
    added_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)  REFERENCES users(user_id)  ON DELETE CASCADE,
    FOREIGN KEY (stock_id) REFERENCES stocks(stock_id) ON DELETE CASCADE,
    UNIQUE KEY uq_user_stock (user_id, stock_id)  -- prevent duplicates
) ENGINE=InnoDB;

-- =============================================================
-- End of schema
-- =============================================================
