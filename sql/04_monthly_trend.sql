-- Monthly volume and on-time rate, with month-over-month change in volume.
WITH monthly AS (
    SELECT month,
           SUM(pallets)                   AS pallets,
           ROUND(100.0 * AVG(on_time), 1) AS on_time_pct
    FROM v_delivered
    GROUP BY month
)
SELECT month,
       pallets,
       on_time_pct,
       pallets - LAG(pallets) OVER (ORDER BY month) AS pallets_change
FROM monthly
ORDER BY month;
