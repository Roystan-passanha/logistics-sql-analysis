-- Does the Oct-Nov peak hurt service? Compare peak with the rest of the year per region.
SELECT region,
       ROUND(100.0 * AVG(CASE WHEN CAST(strftime('%m', planned_date) AS INTEGER) IN (10, 11) THEN on_time END), 1) AS peak_on_time_pct,
       ROUND(100.0 * AVG(CASE WHEN CAST(strftime('%m', planned_date) AS INTEGER) NOT IN (10, 11) THEN on_time END), 1) AS rest_on_time_pct
FROM v_delivered
GROUP BY region
ORDER BY peak_on_time_pct;
