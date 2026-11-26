-- =====================================================
-- PROJECT: Olist E-commerce Analytics
-- FILE: Geographic Analysis
-- PURPOSE: Compare state-wise orders, payment value,
--          average order value and delivery performance
-- =====================================================


-- 1. State-wise Business Performance

SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS total_orders,

    ROUND(
        SUM(total_payment_value), 2
    ) AS total_payment_value,

    ROUND(
        AVG(total_payment_value), 2
    ) AS average_order_value,

    ROUND(
        AVG(delivery_days), 2
    ) AS average_delivery_days,

    ROUND(
        100.0 * SUM(delivery_delay_days > 0)
        / NULLIF(COUNT(delivery_delay_days), 0),
        2
    ) AS delay_percentage

FROM order_level_analytics
WHERE customer_state IS NOT NULL
GROUP BY customer_state
ORDER BY total_orders DESC;