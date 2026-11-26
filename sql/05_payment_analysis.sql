-- =====================================================
-- PROJECT: Olist E-commerce Analytics
-- FILE: Payment Analysis
-- PURPOSE: Analyse payment methods and credit card
--          installment behaviour
-- =====================================================


-- 1. Payment Method Distribution

SELECT
    payment_type,
    COUNT(*) AS total_payment_records,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(payment_value), 2) AS total_payment_value,
    ROUND(AVG(payment_value), 2) AS average_payment_record,
    ROUND(
        100.0 * COUNT(DISTINCT order_id)
        / (
            SELECT COUNT(DISTINCT order_id)
            FROM order_level_analytics
        ),
        2
    ) AS order_percentage
FROM order_payments
GROUP BY payment_type
ORDER BY total_orders DESC;


-- 2. Credit Card Installment Analysis

SELECT
    payment_installments,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(payment_value), 2) AS total_payment_value,
    ROUND(AVG(payment_value), 2) AS average_payment_record
FROM order_payments
WHERE payment_type = 'credit_card'
GROUP BY payment_installments
ORDER BY payment_installments;


-- 3. Average Credit Card Payment by Installment

WITH order_installments AS (
    SELECT
        order_id,
        payment_installments,
        SUM(payment_value) AS order_payment_value
    FROM order_payments
    WHERE payment_type = 'credit_card'
    GROUP BY
        order_id,
        payment_installments
)

SELECT
    payment_installments,
    COUNT(*) AS order_installment_groups,
    ROUND(SUM(order_payment_value), 2) AS total_payment_value,
    ROUND(AVG(order_payment_value), 2) AS average_credit_card_payment
FROM order_installments
GROUP BY payment_installments
ORDER BY payment_installments;