-- Tables for the delivery log. Loaded from data/*.csv by run_analysis.py.
CREATE TABLE warehouses (
    warehouse_id TEXT PRIMARY KEY,
    region       TEXT NOT NULL,
    city         TEXT NOT NULL
);

CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    segment     TEXT NOT NULL
);

CREATE TABLE deliveries (
    delivery_id  TEXT PRIMARY KEY,
    warehouse_id TEXT NOT NULL REFERENCES warehouses (warehouse_id),
    customer_id  TEXT NOT NULL REFERENCES customers (customer_id),
    planned_date DATE NOT NULL,
    actual_date  DATE,               -- NULL when cancelled
    pallets      INTEGER NOT NULL,
    status       TEXT NOT NULL,      -- Delivered | Cancelled
    late_reason  TEXT                -- NULL when on time
);

-- One row per completed delivery with lateness worked out once.
CREATE VIEW v_delivered AS
SELECT d.*,
       w.region,
       c.segment,
       CAST(julianday(d.actual_date) - julianday(d.planned_date) AS INTEGER) AS days_late,
       CASE WHEN d.actual_date <= d.planned_date THEN 1 ELSE 0 END          AS on_time,
       strftime('%Y-%m', d.planned_date)                                     AS month
FROM deliveries d
JOIN warehouses w USING (warehouse_id)
JOIN customers  c USING (customer_id)
WHERE d.status = 'Delivered';
