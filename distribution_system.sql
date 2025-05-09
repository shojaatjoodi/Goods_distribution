-- 1. Create or recreate the database
DROP DATABASE IF EXISTS distribution_system;
CREATE DATABASE distribution_system;
USE distribution_system;

-- 2. Create Suppliers table
CREATE TABLE Suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(255)
);

-- 3. Create Companies table
CREATE TABLE Companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(255)
);

-- 4. Create Citizens table
CREATE TABLE Citizens (
    citizen_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    national_id VARCHAR(20) UNIQUE NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(20),
    eligible BOOLEAN DEFAULT TRUE
);

-- 5. Create Goods table
CREATE TABLE Goods (
    good_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    stock_quantity INT DEFAULT 0
);

-- 6. Create Deliveries table
CREATE TABLE Deliveries (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    good_id INT,
    supplier_id INT,
    company_id INT,
    quantity_received INT,
    delivery_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (good_id) REFERENCES Goods(good_id) ON DELETE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id) ON DELETE SET NULL,
    FOREIGN KEY (company_id) REFERENCES Companies(company_id) ON DELETE SET NULL
);

-- 7. Create Distributions table
CREATE TABLE Distributions (
    distribution_id INT AUTO_INCREMENT PRIMARY KEY,
    citizen_id INT,
    good_id INT,
    company_id INT,
    quantity_given INT,
    distribution_date DATETIME, 
    FOREIGN KEY (citizen_id) REFERENCES Citizens(citizen_id) ON DELETE CASCADE,
    FOREIGN KEY (good_id) REFERENCES Goods(good_id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES Companies(company_id) ON DELETE SET NULL
);

    -- distribution_date DATETIME DEFAULT CURRENT_TIMESTAMP,   -- this is not needed as we will set it manually

-- 8. Prepopulate Goods table
INSERT INTO Goods (name, stock_quantity) VALUES
('Sugar', 0),
('Red Meat', 0),
('Chicken Meat', 0),
('Cheese', 0),
('Rice', 0),
('Spaghetti', 0),
('Tea', 0),
('Oil', 0),
('Beans', 0),
('Egg', 0);






--- ............... adding some fake data for testing purposes ............... 

-- 9. Prepopulate Suppliers table
INSERT INTO Suppliers (name, contact_info) VALUES
('Supplier A', '123-456-7890'),
('Supplier B', '987-654-3210'),
('Supplier C', '555-555-5555'),
('Supplier D', '444-444-4444'),
('Supplier E', '333-333-3333');

-- 10. Prepopulate Companies table example values are:

--- Company A: 123-456-7890
--- Company B: 987-654-3210
--- Company C: 555-555-5555
--- Company D: 444-444-4444
--- Company E: 333-333-3333
-- inserting example values for companies
INSERT INTO Companies (name, contact_info) VALUES
('Company A', '123-456-7890'),
('Company B', '987-654-3210'),
('Company C', '555-555-5555'),
('Company D', '444-444-4444'),
('Company E', '333-333-3333');

-- 11. Prepopulate Citizens table example values are:
--- Citizen A: 1234567890
--- Citizen B: 9876543210
--- Citizen C: 5555555555
--- Citizen D: 4444444444
--- Citizen E: 3333333333
-- inserting example values for citizens
INSERT INTO Citizens (name, national_id, address, phone, eligible) VALUES
('Citizen A', '1234567890', '123 Main St', '555-111-2222', TRUE),
('Citizen B', '9876543210', '456 Elm St', '555-222-3333', TRUE),
('Citizen C', '5555555555', '789 Oak St', '555-333-4444', TRUE),
('Citizen D', '4444444444', '101 Pine St', '555-444-5555', TRUE),
('Citizen E', '3333333333', '202 Maple St', '555-555-6666', TRUE);

-- 12. Prepopulate Deliveries table example values are:
--- Delivery A: 1234567890  
--- Delivery B: 9876543210
--- Delivery C: 5555555555
--- Delivery D: 4444444444
--- Delivery E: 3333333333
-- inserting example values for deliveries
INSERT INTO Deliveries (good_id, supplier_id, company_id, quantity_received) VALUES
(1, 1, 1, 100),
(2, 2, 2, 200),
(3, 3, 3, 150),
(4, 4, 4, 50),
(5, 5, 5, 300);

-- 13. Prepopulate Distributions table example values are:
--- Distribution A: 1234567890
--- Distribution B: 9876543210
--- Distribution C: 5555555555
--- Distribution D: 4444444444
--- Distribution E: 3333333333
-- inserting example values for distributions
INSERT INTO Distributions (citizen_id, good_id, company_id, quantity_given) VALUES
(1, 1, 1, 10),
(2, 2, 2, 20),
(3, 3, 3, 15),
(4, 4, 4, 5),
(5, 5, 5, 30);




