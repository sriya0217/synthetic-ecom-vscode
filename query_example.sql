-- query_example.sql
SELECT
  o.order_id,
  o.order_date,
  o.customer_id,
  c.name AS customer_name,
  COUNT(oi.order_item_id) AS items_in_order,
  SUM(oi.total_price) AS total_amount,
  o.discount,
  o.final_amount,
  GROUP_CONCAT(DISTINCT p.category) AS categories
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.order_status = 'Delivered'
GROUP BY o.order_id
ORDER BY o.order_date DESC
LIMIT 200;
