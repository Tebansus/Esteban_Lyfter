BEGIN;

SET search_path TO lyfter_products;

-- Create the tables for the transaction testing

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,                
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL,
    in_inventory INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    total_cost DECIMAL(12, 2) NOT NULL,
	state_of_invoice VARCHAR(20) DEFAULT 'COMPLETED',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Insert 2 users for testing purposes on the transaction front

INSERT INTO users (name, email, username, password, phone)
VALUES 
    ('Alice Example', 'alice@example.com', 'alice', 'hashed_password_1', '123-456-7890'),
    ('Bob Tester', 'bob@example.com', 'bob', 'hashed_password_2', '987-654-3210')
ON CONFLICT (email) DO NOTHING;

-- Insert the 2 products to match the users for transaction testing

INSERT INTO products (name, category, price, in_inventory)
VALUES 
    ('Hatchet', 'Tool', 20, 10),
    ('Apple', 'Food', 30, 5);


COMMIT;

-- Transaction to create an invoice for a user purchasing a product
-- This transaction checks if the user exists, if the product is available in sufficient quantity, and then creates an invoice while updating the inventory.
-- If any condition fails, it raises an exception to roll back the transaction. It uses the DO block to encapsulate the logic in a single transaction.

BEGIN;
SET search_path TO lyfter_products;

DO $$
DECLARE
    product_price numeric;
BEGIN
    IF EXISTS (
        SELECT 1 FROM users WHERE id = 2
    ) AND EXISTS (
        SELECT 1 FROM products WHERE id = 2 AND in_inventory >= 2
    ) THEN
        -- Get price
        SELECT price INTO product_price FROM products WHERE id = 2;

        -- Insert invoice
        INSERT INTO invoices (user_id, product_id, quantity, unit_price, total_cost)
        VALUES (2, 2, 2, product_price, product_price * 2);

        -- Update inventory
        UPDATE products
        SET in_inventory = in_inventory - 2
        WHERE id = 2;
    ELSE
        RAISE EXCEPTION 'User or product not found, or insufficient inventory';
    END IF;

    -- Check if invoice was created
    IF EXISTS(
        SELECT 1 FROM invoices WHERE user_id = 2 AND product_id = 2 AND quantity = 2
    ) THEN
        RAISE NOTICE 'Transaction created successfully';
    ELSE
        RAISE EXCEPTION 'Transaction creation failed';
    END IF;
END $$;

COMMIT;


--Second part of the transaction to return an item
-- This transaction checks if the user has a completed invoice for the product they want to return.
BEGIN;
SET search_path TO lyfter_products;

DROP TABLE IF EXISTS _inv_to_return;
CREATE TEMP TABLE _inv_to_return AS
SELECT id            AS invoice_id,
       product_id,
       quantity
FROM   invoices
WHERE  user_id          = 2            
  AND  product_id       = 2            
  AND  quantity         = 2            
  AND  state_of_invoice = 'COMPLETED'  
ORDER  BY id DESC                      
LIMIT  1
FOR UPDATE;                            

-- If nothing was selected, abort the whole transaction
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM _inv_to_return) THEN
        RAISE EXCEPTION
          'Return failed: matching completed invoice not found.';
    END IF;
END $$;

--Put the return logic here to update the inventory quantity to reflect the return
UPDATE products p
SET    in_inventory = in_inventory + t.quantity
FROM   _inv_to_return t
WHERE  p.id = t.product_id;

-- Update the invoice state to 'RETURNED'
UPDATE invoices i
SET    state_of_invoice = 'RETURNED'
FROM   _inv_to_return t
WHERE  i.id = t.invoice_id;

-- Select the invoice to return
SELECT *
FROM   invoices
WHERE  id = (SELECT invoice_id FROM _inv_to_return);

COMMIT;