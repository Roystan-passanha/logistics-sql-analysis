-- Top late reason per region and its share of that region's late deliveries.
WITH reasons AS (
    SELECT region,
           late_reason,
           COUNT(*) AS late_count,
           SUM(COUNT(*)) OVER (PARTITION BY region) AS region_late_total
    FROM v_delivered
    WHERE on_time = 0
    GROUP BY region, late_reason
),
ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY region ORDER BY late_count DESC) AS rn
    FROM reasons
)
SELECT region,
       late_reason                                      AS top_reason,
       late_count,
       ROUND(100.0 * late_count / region_late_total, 1) AS share_of_region_late_pct
FROM ranked
WHERE rn = 1
ORDER BY late_count DESC;
