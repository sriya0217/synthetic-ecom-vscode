A-SDLC

To upload a local project to GitHub, the first step is to create a new repository on GitHub. Log in to your GitHub account, click on the “New Repository” button, and give your repository a name, for example, synthetic-ecom-vscode. You can choose to make it public or private, depending on whether you want others to see it. Do not initialize it with a README if you already have one locally. Once created, GitHub will provide you with the repository URL, which you will use to link your local project.

Next, open your project folder on your local machine. If it’s not already a Git repository, initialize it using the command git init. This sets up a local Git repository and allows you to track changes in your project. After initializing, add all your project files to the staging area using git add ., and then commit them with a meaningful message, for example, git commit -m "Initial commit: data generator, SQLite ingestion, example query". Committing saves a snapshot of your project in the local Git repository.

After committing your files locally, you need to link your local repository to the GitHub repository you created. You do this by setting the remote URL using the command git remote add origin https://github.com/yourusername/synthetic-ecom-vscode.git, replacing yourusername with your GitHub username. You can verify the remote link using git remote -v.

Finally, push your local commits to GitHub using the command git push -u origin main. The first time you push, Git might ask for authentication. Since GitHub no longer supports passwords for HTTPS, you need to use a Personal Access Token (PAT) as your password. After entering your username and PAT, Git will upload your project to GitHub. From that point onward, your local repository is synced with GitHub, and any future changes can be committed and pushed using the same workflow.

using an LLM inside VS Code :

If you intended to ask an LLM for the generation and ingestion prompts (as the exercise originally required), here are the exact prompts you could paste to an LLM (or keep for documentation):

Prompt A — generate synthetic ecom data:
Generate 5 separate CSV files for synthetic e-commerce data: customers (5000), products (2000), orders (20000), order_items (50000), reviews (8000). Ensure referential integrity, realistic prices/discounts, dates YYYY-MM-DD, small seasonality spikes in Nov-Dec, and human-like review_texts. Output should be downloadable files customers.csv, products.csv, orders.csv, order_items.csv, reviews.csv.


Prompt B — ingest into sqlite:
Given CSV files customers.csv, products.csv, orders.csv, order_items.csv, reviews.csv, create a SQLite database named ecom.db. Create tables with appropriate types, load CSV data, and add helpful indices for joins. Provide the SQL or a Python script using pandas.to_sql.


Prompt C — generate a SQL join:
Write an SQL query that joins orders, order_items, products and customers to return for each delivered order: order_id, order_date, customer_name, item_count, total_amount, discount, final_amount, list_of_categories. Limit output to 200 rows ordered by order_date desc.
