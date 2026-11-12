-- Customers with the most late pallets (minimum 50 deliveries), for account managers.
SELECT customer_id,
       segment,
       COUNT(*)                                        AS deliveries,
       SUM(CASE WHEN on_time = 0 THEN pallets ELSE 0 END) AS late_pallets,
       ROUND(100.0 * AVG(on_time), 1)                  AS on_time_pct
FROM v_delivered
GROUP BY customer_id, segment
HAVING COUNT(*) >= 50
ORDER BY late_pallets DESC
LIMIT 10;
