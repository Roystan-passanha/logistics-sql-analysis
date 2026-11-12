-- Overall KPIs for the year.
SELECT COUNT(*)                                  AS deliveries,
       SUM(pallets)                              AS pallets,
       ROUND(100.0 * AVG(on_time), 1)            AS on_time_pct,
       ROUND(AVG(CASE WHEN on_time = 0 THEN days_late END), 2) AS avg_days_late_when_late,
       (SELECT COUNT(*) FROM deliveries WHERE status = 'Cancelled') AS cancelled
FROM v_delivered;
