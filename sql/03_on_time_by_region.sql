-- On-time rate by region, ranked. Which warehouse needs attention first?
SELECT region,
       COUNT(*)                               AS deliveries,
       SUM(pallets)                           AS pallets,
       ROUND(100.0 * AVG(on_time), 1)         AS on_time_pct,
       SUM(1 - on_time)                       AS late_deliveries,
       RANK() OVER (ORDER BY AVG(on_time))    AS attention_rank
FROM v_delivered
GROUP BY region
ORDER BY attention_rank;
