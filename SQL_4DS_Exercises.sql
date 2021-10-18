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

--- Chapter 6: Aggregations

SELECT
	market_date,
    customer_id
FROM farmers_market.customer_purchases
GROUP BY market_date, customer_id
ORDER BY market_date, customer_id

--- group summaries
-- count the rows in the customer_purchases table per market date per customer
SELECT
	market_date,
    customer_id,
    COUNT(*) AS items_purchased
FROM farmers_market.customer_purchases
GROUP BY market_date, customer_id
ORDER BY market_date, customer_id
LIMIT 10

-- sum up the quantity column
SELECT
	market_date,
    customer_id,
    SUM(quantity) AS items_purchased
FROM farmers_market.customer_purchases
GROUP BY market_date, customer_id
ORDER BY market_date, customer_id
LIMIT 10

-- kinds of items purchased per customer on each market date
SELECT
	market_date,
    customer_id,
    COUNT( DISTINCT product_id) AS different_products_purchased
FROM farmers_market.customer_purchases AS c
GROUP BY market_date, customer_id
ORDER BY market_date, customer_id
LIMIT 10

-- single query for summaries
--- summarizing per market date per customer id
SELECT
	market_date,
    customer_id,
	SUM(quantity) AS items_purchased,
    COUNT( DISTINCT product_id) AS different_products_purchased
FROM farmers_market.customer_purchases AS c
GROUP BY market_date, customer_id
ORDER BY market_date, customer_id
LIMIT 10

--- calculations inside aggregate functions
SELECT
	market_date,
    customer_id,
	vendor_id,
    quantity * cost_to_customer_per_qty AS price
FROM farmers_market.customer_purchases AS c
WHERE customer_id = 3
ORDER BY market_date, vendor_id

--- customer spend total on market date
SELECT
	customer_id,
    market_date,
	vendor_id,
    SUM(quantity * cost_to_customer_per_qty) AS total_spent
FROM farmers_market.customer_purchases AS c
WHERE customer_id = 3
GROUP BY market_date
ORDER BY market_date

---adding customer_id to groupby to see by vendor
SELECT
	customer_id,
	vendor_id,
    SUM(quantity * cost_to_customer_per_qty) AS total_spent
FROM farmers_market.customer_purchases AS c
WHERE customer_id = 3
GROUP BY customer_id, vendor_id
ORDER BY customer_id, vendor_id

--- list of every customer and how much they have spent at the farmers market
SELECT
	customer_id,
	SUM(quantity * cost_to_customer_per_qty) AS total_spent
FROM farmers_market.customer_purchases
GROUP BY customer_d
ORDER BY customer_id

--- join tables to bring in details
SELECT c.customer_first_name,
	c.customer_last_name,
	cp.customer_id,
	v.vendor_name,
	cp.vendor_id,
	cp.quantity * cp.cost_to_customer_per_qty AS price
FROM farmers_market.customer AS c

LEFT JOIN farmers_market.customer_purchases AS cp
	ON c.customer_id = cp.customer_id
LEFT JOIN farmers_market.vendor AS v
	ON cp.vendor_id = v.vendor_id
WHERE cp.customer_id = 3
ORDER BY cp.customer_id, cp.vendor_id

--- summarize at the level of one row per customer per vendor
SELECT c.customer_first_name,
	c.customer_last_name,
	cp.customer_id,
	v.vendor_name,
	cp.vendor_id,
	ROUND(SUM(quantity * cost_to_customer_per_qty), 2) AS total_spent
	
FROM farmers_market.customer AS c

LEFT JOIN farmers_market.customer_purchases AS cp
	ON c.customer_id = cp.customer_id
LEFT JOIN farmers_market.vendor AS v
	ON cp.vendor_id = v.vendor_id
WHERE cp.customer_id = 3
GROUP BY 
	c.customer_first_name,
	c.customer_last_name,
	cp.customer_id,
	v.vendor_name,
	cp.vendor_id
ORDER BY cp.customer_id, cp.vendor_id

--- filter to single vendor
SELECT c.customer_first_name,
	c.customer_last_name,
	cp.customer_id,
	v.vendor_name,
	cp.vendor_id,
	ROUND(SUM(quantity * cost_to_customer_per_qty), 2) AS total_spent
	
FROM farmers_market.customer AS c

LEFT JOIN farmers_market.customer_purchases AS cp
	ON c.customer_id = cp.customer_id
LEFT JOIN farmers_market.vendor AS v
	ON cp.vendor_id = v.vendor_id
WHERE cp.customer_id = 9
GROUP BY 
	c.customer_first_name,
	c.customer_last_name,
	cp.customer_id,
	v.vendor_name,
	cp.vendor_id
ORDER BY cp.customer_id, cp.vendor_id

--- Min/Max
SELECT *
FROM farmers_market.vendor_inventory
ORDER BY original_price
LIMIT 10

--- least and most expensive in table
SELECT
	MIN(original_price) AS minimum_price,
	MAX(original_price) AS maximum_price
FROM farmers_market.vendor_inventory
ORDER BY original_price

--- lowest and highest prices in category
SELECT
	pc.product_category_name,
	p.product_category_id,
	MIN(vi.original_price) AS minimum_price,
	MAX(vi.original_price) AS maximum_price
FROM farmers_market.vendor_inventory AS vi
INNER JOIN farmers_market.product AS p
	ON vi.product_id = p.product_id
INNER JOIN farmersmarket.product_category AS pc
	ON p.product_category_id = pc.product_category_id
GROUP BY pc.product_category_name, p.product_category_id

--- COUNT AND COUNT DISTINCT
SELECT market_date, COUNT(product_id) AS product_count
FROM  farmers_market.vendor_inventory
GROUP BY market_date
ORDER BY market_date

--- how many diff products with unique products IDS each vendor bought
SELECT vendor_id,
	COUNT(DISTINCT product_id) AS diff_prods_offered
FROM farmers_market.vendor_inventory
WHERE market_date BETWEEN '2019-03-02' AND '2019-03-16'
GROUP BY vendor_id
ORDER BY vendor_id

--- Average
SELECT vendor_id,
	COUNT(DISTINCT product_id) AS diff_prods_offered,
	AVG(original_price) AS avg_prod_price
	
FROM farmers_market.vendor_inventory
WHERE market_date BETWEEN '2019-03-02' AND '2019-03-16'
GROUP BY vendor_id
ORDER BY vendor_id


--- true average price of items in each vendors inventory between dates
SELECT vendor_id,
	COUNT(DISTINCT product_id) AS diff_prods_offered,
	SUM(quantity * original_price) AS value_of_inventory,
	SUM(quantity) AS inventory_item_count,
	ROUND(SUM(quantity * original_price) / SUM(quantity), 2) AS average_item_price
	
FROM farmers_market.vendor_inventory
WHERE market_date BETWEEN '2019-03-02' AND '2019-03-16'
GROUP BY vendor_id
ORDER BY vendor_id

---- Filtering with HAVING
SELECT 
	vendor_id,
	
	COUNT(DISTINCT product_id) AS diff_prods_offered,
	
	SUM(quantity * original_price) AS value_of_inventory,
	
	SUM(quantity) AS inventory_item_count,
	
	ROUND(SUM(quantity * original_price) / SUM(quantity), 2) AS average_item_price
	
FROM farmers_market.vendor_inventory
WHERE market_date BETWEEN '2019-03-02' AND '2019-03-16'
GROUP BY vendor_id
HAVING inventory_item_count>=100
ORDER BY vendor_id


--- CASE inside Aggregate functions
SELECT
	cp.market_date,
	cp.vendor_id,
	cp.customer_id,
	cp.product_id,
	cp.quantity,
	p.product_name,
	p.product_size,
	p.product_qty_type
FROM farmers_market.customer_purchases AS cp
INNER JOIN farmers_market.product AS p
	ON cp.product_id = p.product_id
	
--- one column that adds up quantities of products that are sold by unit and another that adds up quantities of prodeucts sold by pound
SELECT
	cp.market_date,
	cp.vendor_id,
	cp.customer_id,
	cp.product_id,
	CASE WHEN product_qty_type = "unit" THEN quantity ELSE 0 END AS quantity_units,
	CASE WHEN product_qty_type = "lbs" THEN quantity ELSE 0 END AS quantity_lbs,
	CASE WHEN product_qty_type NOT IN ("unit", "lbs") THEN quantity ELSE 0 END AS quantity_other,
	p.product_qty_type
FROM farmers_market.customer_purchases AS cp
INNER JOIN farmers_market.product AS p
	ON cp.product_id = p.product_id
	

SELECT
	cp.market_date,
	cp.vendor_id,
	cp.customer_id,
	cp.product_id,
	CASE WHEN product_qty_type = "unit" THEN quantity ELSE 0 END AS quantity_units_purchased,
	CASE WHEN product_qty_type = "lbs" THEN quantity ELSE 0 END AS quantity_lbs_purchased,
	CASE WHEN product_qty_type NOT IN ("unit", "lbs") THEN quantity ELSE 0 END AS quantity_other,
	p.product_qty_type
FROM farmers_market.customer_purchases AS cp
INNER JOIN farmers_market.product AS p
	ON cp.product_id = p.product_id


--- Ch 6. Exercises: query that determines how many times each vendor has rented a booth at the farmers market.
SELECT 
	DISTINCT(vendor_id),
	COUNT(market_date) AS days_sold
FROM farmers_market.vendor_booth_assignments
GROUP BY vendor_id
ORDER BY vendor_id

------------------------
SELECT 
	fmpc.product_category_name, 
	fmp.product_name,
    MIN(fmcp.market_date) AS earliest_date_available,
	MAX(fmcp.market_date) AS latest_date_available
    
FROM farmers_market.customer_purchases AS fmcp

LEFT JOIN farmers_market.product AS fmp
	ON fmcp.product_id = fmp.product_id
    
LEFT JOIN farmers_market.product_category AS fmpc
	ON fmp.product_category_id = fmpc.product_category_id 

GROUP BY 
	fmpc.product_category_name,
    fmp.product_name

HAVING fmpc.product_category_name = "Fresh Fruits & Vegetables"

----------------
SELECT 
	fmc.customer_last_name,
    	fmc.customer_first_name,
	SUM(fmcp.quantity * fmcp.cost_to_customer_per_qty) AS spend

FROM farmers_market.customer AS fmc

JOIN farmers_market.customer_purchases AS fmcp
	ON fmcp.customer_id = fmc.customer_id

GROUP BY 
	fmc.customer_last_name,
    fmc.customer_first_name
    
ORDER BY fmc.customer_last_name
	
