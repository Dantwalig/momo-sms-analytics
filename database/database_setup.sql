CREATE DATABASE IF NOT EXISTS `momo-sms-analytics`;
USE `momo-sms-analytics`;


CREATE TABLE Category (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Primary Key for the category',
    category_name VARCHAR(100) NOT NULL UNIQUE COMMENT 'Display name of the category',
    description VARCHAR(255) COMMENT 'Detailed description of what this category covers',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when category was created'
) ENGINE=InnoDB;


CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Primary Key for the user',
    phone_number VARCHAR(20) NOT NULL UNIQUE COMMENT 'Unique mobile number',
    contact_name VARCHAR(150) COMMENT 'Name as it appears in contacts',
    user_type VARCHAR(50) COMMENT 'Classification: Individual, Merchant, or Agent',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when user record was created'
) ENGINE=InnoDB;


CREATE TABLE Transaction (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Primary Key for the transaction',
    category_id INT COMMENT 'FK to Category table',
    transaction_reference VARCHAR(100) UNIQUE NOT NULL COMMENT 'Unique reference code from the SMS (e.g., ID: 123456789)',
    amount DECIMAL(15, 2) NOT NULL COMMENT 'Monetary value of the transaction',
    transaction_type VARCHAR(50) COMMENT 'Type e.g., DEBIT, CREDIT',
    transaction_status VARCHAR(50) DEFAULT 'Completed' COMMENT 'Status e.g., Pending, Completed, Failed',
    transaction_date DATETIME NOT NULL COMMENT 'The date/time extracted from the SMS',
    raw_sms_body TEXT COMMENT 'The original SMS content for auditing',
    
    CONSTRAINT fk_transaction_category 
        FOREIGN KEY (category_id) REFERENCES Category(category_id) 
        ON DELETE SET NULL,
    CONSTRAINT chk_positive_amount CHECK (amount >= 0)
) ENGINE=InnoDB;


CREATE TABLE Role (
    role_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Primary Key for the role assignment',
    user_id INT NOT NULL COMMENT 'FK to User',
    transaction_id INT NOT NULL COMMENT 'FK to Transaction',
    role_type VARCHAR(20) NOT NULL COMMENT 'Sender or Receiver',
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of assignment',
    
    CONSTRAINT fk_role_user FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_role_transaction FOREIGN KEY (transaction_id) REFERENCES Transaction(transaction_id) ON DELETE CASCADE,
    CONSTRAINT chk_role_type CHECK (role_type IN ('sender', 'receiver'))
) ENGINE=InnoDB;


CREATE TABLE System_Log (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Primary Key for the log entry',
    transaction_id INT NOT NULL COMMENT 'FK to Transaction',
    log_status VARCHAR(50) COMMENT 'Status of the system log entry',
    service_center VARCHAR(100) COMMENT 'The SMS service center address',
    readable_date VARCHAR(100) COMMENT 'Original date string as found in SMS',
    logged_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'System timestamp when logged',
    
    CONSTRAINT fk_log_transaction FOREIGN KEY (transaction_id) REFERENCES Transaction(transaction_id) ON DELETE CASCADE
) ENGINE=InnoDB;


CREATE INDEX idx_user_phone ON User(phone_number);

CREATE INDEX idx_transaction_date ON Transaction(transaction_date);

CREATE INDEX idx_role_user_lookup ON Role(user_id, role_type);

CREATE INDEX idx_log_transaction ON System_Log(transaction_id);


INSERT INTO Category (category_name, description) VALUES
('P2P Transfer', 'Person to person money transfer'),
('Airtime Top-up', 'Purchase of mobile airtime'),
('Merchant Payment', 'Payments made to retail stores'),
('Cash Out', 'Withdrawals at agent locations'),
('Utility Bill', 'Payments for water, electricity, etc.');

INSERT INTO User (phone_number, contact_name, user_type) VALUES
('250780000001', 'Alice Munyaneza', 'Individual'),
('250780000002', 'Wakuma Kamana', 'Individual'),
('250780000003', 'Supermarket Ltd', 'Merchant'),
('250780000004', 'Agent John', 'Agent'),
('250780000005', 'Charlie Umutoni', 'Individual');

INSERT INTO Transaction (category_id, transaction_reference, amount, transaction_type, transaction_status, transaction_date, raw_sms_body) VALUES
(1, 'TXN998877', 5000.00, 'DEBIT', 'Completed', '2026-01-20 10:30:00', 'You have sent 5000 RWF to Alice Munyaneza...'),
(2, 'TXN112233', 1000.00, 'DEBIT', 'Completed', '2026-01-21 14:15:00', 'Airtime purchase of 1000 RWF successful...'),
(3, 'TXN445566', 15500.50, 'DEBIT', 'Completed', '2026-01-22 09:00:00', 'Payment of 15500.5 RWF to Supermarket Ltd...'),
(4, 'TXN778899', 20000.00, 'CREDIT', 'Completed', '2026-01-23 18:45:00', 'Cash out of 20000 RWF at Agent John...'),
(5, 'TXN001122', 12000.00, 'DEBIT', 'Completed', '2026-01-24 08:20:00', 'Bill payment for Water Board... ');

INSERT INTO Role (user_id, transaction_id, role_type) VALUES
(2, 1, 'sender'), (1, 1, 'receiver'), 
(2, 2, 'sender'),                    
(5, 3, 'sender'), (3, 3, 'receiver'),
(4, 4, 'sender'), (2, 4, 'receiver'),
(1, 5, 'sender');

INSERT INTO System_Log (transaction_id, log_status, service_center, readable_date) VALUES
(1, 'Parsed', '+250123', 'Jan 20, 2026 10:30'),
(2, 'Parsed', '+250123', 'Jan 21, 2026 14:15'),
(3, 'Parsed', '+250123', 'Jan 22, 2026 09:00'),
(4, 'Parsed', '+250123', 'Jan 23, 2026 18:45'),
(5, 'Parsed', '+250123', 'Jan 24, 2026 08:20');