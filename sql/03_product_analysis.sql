-- =====================================================
-- PROJECT: Olist E-commerce Analytics
-- FILE: Product Analysis
-- PURPOSE: Analyse product categories, sales, pricing,
--          customer reviews and delivery performance
-- =====================================================


-- 1. Top 10 Product Categories by Sales

SELECT
    p.product_category_name,
    COUNT(*) AS total_items_sold,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS product_sales,
    ROUND(SUM(oi.freight_value), 2) AS freight_value
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY product_sales DESC
LIMIT 10;


-- 2. Product Category Sales Contribution (%)

SELECT
    product_category_name,
    product_sales,
    ROUND(
        100.0 * product_sales
        / SUM(product_sales) OVER (),
        2
    ) AS sales_percentage
FROM (
    SELECT
        p.product_category_name,
        SUM(oi.price) AS product_sales
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE p.product_category_name IS NOT NULL
    GROUP BY p.product_category_name
) AS category_sales
ORDER BY product_sales DESC;


-- 3. Average Item Price by Category
-- Minimum 100 items per category

SELECT
    p.product_category_name,
    COUNT(*) AS total_items,
    ROUND(SUM(oi.price), 2) AS product_sales,
    ROUND(AVG(oi.price), 2) AS average_item_price
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
HAVING COUNT(*) >= 100
ORDER BY average_item_price DESC;


-- 4. Average Review Score by Product Category

WITH order_category AS (
    SELECT DISTINCT
        oi.order_id,
        p.product_category_name
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE p.product_category_name IS NOT NULL
),

category_reviews AS (
    SELECT
        oc.product_category_name,
        oa.order_id,
        oa.average_review_score
    FROM order_category oc
    JOIN order_level_analytics oa
        ON oc.order_id = oa.order_id
    WHERE oa.average_review_score IS NOT NULL
)

SELECT
    product_category_name,
    COUNT(*) AS reviewed_orders,
    ROUND(AVG(average_review_score), 2) AS average_review_score
FROM category_reviews
GROUP BY product_category_name
HAVING COUNT(*) >= 100
ORDER BY average_review_score DESC;


-- 5. Poor Review Percentage by Category
-- Poor review defined as score <= 2

WITH order_category AS (
    SELECT DISTINCT
        oi.order_id,
        p.product_category_name
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE p.product_category_name IS NOT NULL
),

category_reviews AS (
    SELECT
        oc.product_category_name,
        oa.order_id,
        oa.average_review_score
    FROM order_category oc
    JOIN order_level_analytics oa
        ON oc.order_id = oa.order_id
    WHERE oa.average_review_score IS NOT NULL
)

SELECT
    product_category_name,
    COUNT(*) AS reviewed_orders,
    SUM(average_review_score <= 2) AS poor_review_orders,
    ROUND(
        100.0 * SUM(average_review_score <= 2)
        / COUNT(*),
        2
    ) AS poor_review_percentage
FROM category_reviews
GROUP BY product_category_name
HAVING COUNT(*) >= 100
ORDER BY poor_review_percentage DESC;


-- 6. Delivery Delay Percentage by Category

WITH order_category AS (
    SELECT DISTINCT
        oi.order_id,
        p.product_category_name
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE p.product_category_name IS NOT NULL
),

category_delivery AS (
    SELECT
        oc.product_category_name,
        oa.order_id,
        oa.delivery_delay_days,
        oa.average_review_score
    FROM order_category oc
    JOIN order_level_analytics oa
        ON oc.order_id = oa.order_id
    WHERE oa.delivery_delay_days IS NOT NULL
)

SELECT
    product_category_name,
    COUNT(*) AS total_orders,
    SUM(delivery_delay_days > 0) AS delayed_orders,
    ROUND(
        100.0 * SUM(delivery_delay_days > 0)
        / COUNT(*),
        2
    ) AS delay_percentage,
    ROUND(AVG(average_review_score), 2) AS average_review_score
FROM category_delivery
GROUP BY product_category_name
ORDER BY delay_percentage DESC;