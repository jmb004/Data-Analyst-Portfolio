# SQL for Data Scientists Chapter notes and Exercises
# https://www.wiley.com/en-us/SQL+for+Data+Scientists%3A+A+Beginner%27s+Guide+for+Building+Datasets+for+Analysis-p-9781119669388
SELECT *
FROM farmers_market.customer

# all cols and 10 rows
SELECT *
FROM farmers_market.customer
ORDER BY customer_last_name, customer_first_name
LIMIT 10

# all customer IDs and first names in customer table sorted by first_name
SELECT 
	customer_id,
    customer_first_name
FROM farmers_market.customer
ORDER BY customer_first_name


# comment 2
SELECT
	market_date,
    
    customer_id,
    
    vendor_id,
    
    ROUND(quantity * cost_to_customer_per_qty, 2) AS price
    
FROM farmers_market.customer

# WHERE Clause
SELECT
	market_date,
    customer_id,
    vendor_id,
    product_id,
    quantity,
    quantity * cost_to_customer_per_qty AS price
FROM farmers_market.customer_purchases
WHERE customer_id = 4
ORDER BY market_date, vendor_id, product_id
LIMIT 5

# AND/OR operators
SELECT
	market_date,
    customer_id,
    vendor_id,
    product_id,
    quantity,
    quantity * cost_to_customer_per_qty AS price
FROM farmers_market.customer_purchases
WHERE customer_id = 4 OR customer_id = 9
ORDER BY market_date, vendor_id, product_id

SELECT
	market_date,
    customer_id,
    vendor_id,
    product_id,
    quantity,
    quantity * cost_to_customer_per_qty AS price
FROM farmers_market.customer_purchases
WHERE customer_id BETWEEN 8 AND 10
ORDER BY market_date, vendor_id, product_id

# <> operators
SELECT
	market_date,
    customer_id,
    vendor_id,
    product_id,
    quantity,
    quantity * cost_to_customer_per_qty AS price
FROM farmers_market.customer_purchases
WHERE customer_id > 3 AND customer_id <= 5
ORDER BY market_date, customer_id, vendor_id, product_id 

SELECT
	*
FROM farmers_market.vendor_booth_assignments
WHERE vendor_id = 9 AND market_date <= '2019-03-09'
ORDER BY market_date

SELECT
	*
FROM farmers_market.customer
WHERE customer_first_name = 'Carlos' or customer_last_name = 'Diaz'

SELECT 
	market_date,
	transaction_time,
	customer_id,
	vendor_id, 
	quantity
FROM farmers_market.customer_purchases
WHERE customer_id = 1 
	AND vendor_id = 7 
    AND quatity <= 1

# IN
SELECT
	customer_id,
    customer_first_name,
    customer_last_name
FROM farmers_market.customer
WHERE customer_first_name IN ('Renee', 'Rene', 'Renne')

# LIKE
SELECT
	customer_id,
    customer_first_name,
    customer_last_name
FROM farmers_market.customer
WHERE customer_first_name LIKE 'JER%'

# ISNULL
SELECT *
FROM farmers_market.product
WHERE product_size IS NULL

SELECT *
FROM farmers_market.product
WHERE product_size IS NULL OR TRIM(product_size) = ''

# Subqueries for filtering
SELECT 
	market_date, 
	customer_id, 
	vendor_id, 
	quantity * cost_to_customer_per_qty AS price
FROM farmers_market.customer_purchases
WHERE market_date IN 
	( SELECT market_date
    FROM farmers_market.market_date_info
    WHERE market_rain_flag = 1 )
LIMIT 5

# CASE statements
SELECT
	vendor_id,
    vendor_name,
    vendor_type,
    CASE
    WHEN LOWER(vendor_type) LIKE '%fresh%'
    THEN 'Fresh Produce'
    ELSE 'Other'
    END As vendor_type_condensed
    
FROM farmers_market.vendor

# binary flags
SELECT market_date,
market_day
FROM farmers_market.market_date_info
LIMIT 5

SELECT 
	market_date,
	CASE
    WHEN market_day ='Saturday' OR market_day = 'Sunday' THEN 1
    ELSE 0
    END weekend_flag
FROM farmers_market.market_date_info
LIMIT 5
FROM farmers_market.market_date_info
LIMIT 5

# Grouping or binning
SELECT 
	market_date,
	customer_id,
	vendor_id,
	ROUND(quantity * cost_to_customer_per_qty, 2) AS price,
CASE
	WHEN (quantity * cost_to_customer_per_qty > 50) THEN 1
	ELSE 0
	END AS price_over_50
FROM farmers_market.customer_purchases
LIMIT 10

SELECT 
	market_date,
    customer_id,
    vendor_id,
    ROUND(quantity * cost_to_customer_per_qty, 2) AS price,
	CASE
    WHEN (quantity * cost_to_customer_per_qty < 5.00) THEN 'Under $5'
    WHEN (quantity * cost_to_customer_per_qty < 10.00) THEN '$5 - $9.99'
    WHEN (quantity * cost_to_customer_per_qty < 20.00) THEN '$10 - $19.99'
    END price_bin
FROM farmers_market.customer_purchases
LIMIT 10

SELECT 
	market_date,
    customer_id,
    vendor_id,
    ROUND(quantity * cost_to_customer_per_qty, 2) AS price,
	CASE
    WHEN quantity * cost_to_customer_per_qty < 5.00 THEN 5
    WHEN quantity * cost_to_customer_per_qty < 10.00 THEN 10
    WHEN quantity * cost_to_customer_per_qty < 20.00 THEN 20
    END price_bin_lower_end
FROM farmers_market.customer_purchases
LIMIT 10

# categorical encoding
SELECT
	booth_number,
    booth_price_level,
    CASE
    WHEN booth_price_level = 'A' THEN 1
    WHEN booth_price_level = 'B' THEN 2
    WHEN booth_price_level = 'C' THEN 3
    END AS booth_price_level_numeric
FROM farmers_market.booth
LIMIT 5

SELECT
	booth_number,
    booth_price_level,
    CASE WHEN booth_price_level = 'A' THEN 1
	ELSE 0
	END booth_price_level_A,
	CASE WHEN booth_price_level = 'B' THEN 2
	ELSE 0
	END booth_price_level_B,
	CASE WHEN booth_price_level = 'C' THEN 3
	ELSE 0
	END booth_price_level_C
FROM farmers_market.booth
LIMIT 5

# one-hot encoding
SELECT
	vendor_id,
    vendor_name,
    vendor_type,
    CASE
    WHEN vendor_type = 'Arts & Jewelry' THEN 1
    ELSE 0
    END AS vendor_type_arts_jewelry,
    CASE
    WHEN vendor_type = 'Eggs & Meats' THEN 1
    ELSE 0
    END AS vendor_type_eggs_meats,
    CASE
    WHEN vendor_type = 'Fresh Variety: Veggies & More' THEN 1
    ELSE 0
    END AS vendor_type_fresh_variety,
    CASE
    WHEN vendor_type = 'Prepared Foods' THEN 1
    ELSE 0
    END AS vendor_type_prepared
FROM farmers_market.vendor

SELECT
	customer_id,
    CASE
    WHEN customer_zip = '22801' THEN 'Local'
    ELSE 'Not Local'
    END customer_location_type
FROM farmers_market.customer
LIMIT 10

# Ch.4 Exercises
SELECT
	product_id,
    product_name,
CASE WHEN product_qty_type = 'unit' THEN 'unit'
	ELSE 'bulk' 
	END AS prod_qty_type_condensed
FROM farmers_market.product

SELECT
	product_id,
    product_name,
CASE WHEN product_qty_type = 'unit' THEN 'unit'
	ELSE 'bulk' 
	END AS prod_qty_type_condensed,
CASE WHEN product_name LIKE '%pepper%' THEN 1
	ELSE 0
    END pepper_flag
FROM farmers_market.product

# JOINS
SELECT * 
FROM farmers_market.product
LEFT JOIN farmers_market.product_category
	ON farmers_market.product.product_category_id = farmers_market.product_category.product_category_id
    
SELECT * 
FROM farmers_market.product AS fmp
LEFT JOIN farmers_market.product_category AS fmpc
	ON fmp.product_category_id = fmpc.product_category_id
    

    
# INNER JOIN
SELECT *
FROM customer AS c
LEFT JOIN customer_purcahses AS cp
	ON c.customer_id = cp.customer_id
    
SELECT c.*
FROM customer AS c
LEFT JOIN customer_purcahses AS cp
	ON c.customer_id = cp.customer_id
WHERE cp.customer_id IS NULL

SELECT * 
FROM customer AS c
LEFT JOIN customer_purcahses AS cp
	ON c.customer_id = cp.customer_id
WHERE cp.customer_id > 0 # filter out customers without purchase

# RIGHT JOIN
SELECT *
FROM customer AS c
RIGHT JOIN customer_purchases AS cp
	ON c.customer_id = cp.customer_id
    
# filter out by date
SELECT c.*, cp.market_date
FROM customer AS c
LEFT JOIN customer_purchases AS cp
	ON c.customer_id = cp.customer_id
WHERE cp,market_date <> '2019-03-02' OR cp.market_date IS NULL # to get all customers to purchased and did not

# get only a list of customers using DISTINCT
SELECT DISTINCT c.*, cp.market_date
FROM customer AS c
LEFT JOIN customer_purchases AS cp
	ON c.customer_id = cp.customer_id
WHERE cp,market_date <> '2019-03-02' OR cp.market_date IS NULL

# filter to booth, vendor, assignments
SELECT
	b.booth_number,
    b.booth_type,
    vba.market_date,
    v.vendor_id,
    v.vendor_name,
    v.vendor_type
FROM booth AS b
LEFT JOIN vendor_booth_assignments AS vba
	ON b.booth_number = vba.booth_number
LEFT JOIN vendor AS v 
	ON v.vendor_id = vba.vendor_id
ORDER BY b.booth_number, vba.market_date

# Ch. 5 Exercises
SELECT *
FROM vendor AS v
INNER JOIN vendor_booth AS vb
	ON v.vendor_id = vb.vendor_id
ORDER BY v.vendor_name, vb.market_date

SELECT *
FROM customer_purchases AS cp
LEFT JOIN customer AS c
	ON c.customer_id = cp.customer_id

# when of each product is available by type
SELECT
	market_date,
    product_category_name,
    vendor_location
FROM product AS p
LEFT JOIN product_category AS pc
	ON p.product_id = pc.product_id
LEFT JOIN vendor_inventory AS vi
	ON p.vendor_id = vi.vendor_id
WHERE pc.product_category_name = "Fresh Fruit & Vegetable"
ORDER BY market_date




