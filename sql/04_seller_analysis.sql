-- =====================================================
-- PROJECT: Olist E-commerce Analytics
-- FILE: Seller Analysis
-- PURPOSE: Evaluate seller delivery and review
--          performance
-- =====================================================


-- 1. Seller Delivery Performance
-- Considering sellers with at least 50 orders

WITH seller_orders AS (
    SELECT DISTINCT
        seller_id,
        order_id
    FROM order_items
),

seller_performance AS (
    SELECT
        so.seller_id,
        so.order_id,
        oa.delivery_delay_days,
        oa.average_review_score
    FROM seller_orders so
    JOIN order_level_analytics oa
        ON so.order_id = oa.order_id
)

SELECT
    seller_id,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(delivery_delay_days > 0) AS delayed_orders,
    ROUND(
        100.0 * SUM(delivery_delay_days > 0)
        / NULLIF(COUNT(delivery_delay_days), 0),
        2
    ) AS delay_percentage,
    ROUND(AVG(average_review_score), 2) AS average_rating
FROM seller_performance
GROUP BY seller_id
HAVING COUNT(DISTINCT order_id) >= 50
ORDER BY delay_percentage DESC
LIMIT 15;


-- 2. Seller-wise Poor Review Analysis
-- Poor review defined as score <= 2

WITH seller_orders AS (
    SELECT DISTINCT
        seller_id,
        order_id
    FROM order_items
),

seller_performance AS (
    SELECT
        so.seller_id,
        so.order_id,
        oa.average_review_score
    FROM seller_orders so
    JOIN order_level_analytics oa
        ON so.order_id = oa.order_id
    WHERE oa.average_review_score IS NOT NULL
)

SELECT
    seller_id,
    COUNT(*) AS reviewed_orders,
    SUM(average_review_score <= 2) AS poor_review_orders,
    ROUND(
        100.0 * SUM(average_review_score <= 2)
        / COUNT(*),
        2
    ) AS poor_review_percentage,
    ROUND(AVG(average_review_score), 2) AS average_rating
FROM seller_performance
GROUP BY seller_id
HAVING COUNT(*) >= 50
ORDER BY poor_review_percentage DESC
LIMIT 15;