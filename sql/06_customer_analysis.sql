-- =====================================================
-- PROJECT: Olist E-commerce Analytics
-- FILE: Customer Analysis
-- PURPOSE: Analyse one-time and repeat purchasing
--          behaviour
-- =====================================================


-- 1. One-time vs Repeat Customers

WITH customer_orders AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS total_orders
    FROM order_level_analytics
    WHERE customer_unique_id IS NOT NULL
    GROUP BY customer_unique_id
)

SELECT
    CASE
        WHEN total_orders = 1 THEN 'One-time Customer'
        ELSE 'Repeat Customer'
    END AS customer_type,

    COUNT(*) AS total_customers,

    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS customer_percentage,

    ROUND(AVG(total_orders), 2) AS average_orders_per_customer

FROM customer_orders
GROUP BY customer_type;


-- 2. Repeat Purchase Frequency Distribution

WITH customer_orders AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS total_orders
    FROM order_level_analytics
    WHERE customer_unique_id IS NOT NULL
    GROUP BY customer_unique_id
)

SELECT
    total_orders,
    COUNT(*) AS total_customers
FROM customer_orders
WHERE total_orders > 1
GROUP BY total_orders
ORDER BY total_orders;