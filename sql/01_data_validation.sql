-- =====================================================
-- PROJECT: Olist E-commerce Analytics
-- FILE: Data Validation
-- PURPOSE: Validate dataset integrity and consistency
-- =====================================================


-- 1. Total Orders and Duplicate Order IDs

SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT order_id) AS unique_orders
FROM order_level_analytics;


-- 2. Orders Without Customer State

SELECT
    COUNT(*) AS orders_without_state
FROM order_level_analytics
WHERE customer_state IS NULL;


-- 3. Payment Total Reconciliation

SELECT
    (SELECT ROUND(SUM(payment_value), 2)
     FROM order_payments) AS payment_table_total,

    (SELECT ROUND(SUM(total_payment_value), 2)
     FROM order_level_analytics) AS analytics_table_total;


-- 4. Order-Level Payment Mismatch Check

SELECT
    oa.order_id,
    oa.total_payment_value AS analytics_payment,
    SUM(op.payment_value) AS raw_payment
FROM order_level_analytics oa
LEFT JOIN order_payments op
    ON oa.order_id = op.order_id
GROUP BY
    oa.order_id,
    oa.total_payment_value
HAVING
    COUNT(op.order_id) = 0
    OR oa.total_payment_value IS NULL
    OR ABS(
        oa.total_payment_value - SUM(op.payment_value)
    ) > 0.01;


-- 5. Orders Missing Payment Records

SELECT
    oa.order_id,
    oa.order_status,
    oa.total_payment_value,
    oa.order_purchase_timestamp
FROM order_level_analytics oa
LEFT JOIN order_payments op
    ON oa.order_id = op.order_id
WHERE op.order_id IS NULL;