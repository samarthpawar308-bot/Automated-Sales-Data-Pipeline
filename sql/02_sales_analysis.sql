-- =====================================================
-- PROJECT: Olist E-commerce Analytics
-- FILE: Sales Analysis
-- PURPOSE: Analyse monthly sales and order value trends
-- =====================================================


-- 1. Monthly Sales Performance

SELECT
    DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS month,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(total_payment_value), 2) AS total_payment
FROM order_level_analytics
WHERE order_purchase_timestamp IS NOT NULL
GROUP BY month
ORDER BY month;


-- 2. Month-over-Month Payment Growth

WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS month,
        SUM(total_payment_value) AS monthly_payment
    FROM order_level_analytics
    WHERE order_purchase_timestamp IS NOT NULL
    GROUP BY month
),

growth_analysis AS (
    SELECT
        month,
        monthly_payment,
        LAG(monthly_payment) OVER (
            ORDER BY month
        ) AS previous_month_payment
    FROM monthly_sales
)

SELECT
    month,
    ROUND(monthly_payment, 2) AS monthly_payment,
    ROUND(previous_month_payment, 2) AS previous_month_payment,
    ROUND(
        100.0 * (monthly_payment - previous_month_payment)
        / NULLIF(previous_month_payment, 0),
        2
    ) AS growth_percentage
FROM growth_analysis
ORDER BY month;


-- 3. Monthly Average Order Value (AOV)

SELECT
    DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS month,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(total_payment_value), 2) AS total_payment,
    ROUND(
        SUM(total_payment_value)
        / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM order_level_analytics
WHERE order_purchase_timestamp IS NOT NULL
GROUP BY month
ORDER BY month;