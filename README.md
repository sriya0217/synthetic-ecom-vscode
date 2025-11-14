using an LLM inside VS Code (

If you intended to ask an LLM for the generation and ingestion prompts (as the exercise originally required), here are the exact prompts you could paste to an LLM (or keep for documentation):

Prompt A — generate synthetic ecom data:
Generate 5 separate CSV files for synthetic e-commerce data: customers (5000), products (2000), orders (20000), order_items (50000), reviews (8000). Ensure referential integrity, realistic prices/discounts, dates YYYY-MM-DD, small seasonality spikes in Nov-Dec, and human-like review_texts. Output should be downloadable files customers.csv, products.csv, orders.csv, order_items.csv, reviews.csv.


Prompt B — ingest into sqlite:
Given CSV files customers.csv, products.csv, orders.csv, order_items.csv, reviews.csv, create a SQLite database named ecom.db. Create tables with appropriate types, load CSV data, and add helpful indices for joins. Provide the SQL or a Python script using pandas.to_sql.


Prompt C — generate a SQL join:
Write an SQL query that joins orders, order_items, products and customers to return for each delivered order: order_id, order_date, customer_name, item_count, total_amount, discount, final_amount, list_of_categories. Limit output to 200 rows ordered by order_date desc.
