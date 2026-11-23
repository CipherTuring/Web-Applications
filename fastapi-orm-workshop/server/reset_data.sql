-- Workshop 4 - wipe all data and restart the auto-increment counters.
-- Use it before capturing the report screenshots, so the ids and stock
-- values match the ones documented in the report.
--
--   mysql -u ormuser -p orm_workshop < server/reset_data.sql

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE order_items;
TRUNCATE TABLE orders;
TRUNCATE TABLE customers;
TRUNCATE TABLE products;

SET FOREIGN_KEY_CHECKS = 1;
