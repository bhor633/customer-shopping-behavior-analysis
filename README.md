# Customer Shopping Behavior Analysis

End-to-end analytics project for a retail company: **Python** (cleaning and feature engineering) -> **PostgreSQL** (business queries) -> **Power BI** (interactive dashboard).

## Business problem
> How can the company use consumer shopping data to identify trends, improve customer engagement, and optimize marketing and product strategies?

Full brief: 
## 📑 Business Problem Document

[📄 View Business Problem Document (PDF)](https://github.com/bhor633/customer-shopping-behavior-analysis/blob/84e2f9d63a23457d4f2df22d191cbc4998c5172e/customer-shopping-behavior-analysis/customer-shopping-behavior-analysis/docs/Business_Problem_Document.pdf)


## Dataset
3,900 transactions, 18 raw columns: demographics, product, category, purchase amount (USD), season, review rating, subscription, shipping type, discount, payment method, purchase frequency, previous purchases.

## 📁 Dataset

[📊 View Raw Customer Shopping Behavior Dataset (CSV)](https://github.com/bhor633/customer-shopping-behavior-analysis/blob/84e2f9d63a23457d4f2df22d191cbc4998c5172e/customer-shopping-behavior-analysis/customer-shopping-behavior-analysis/data/raw/customer_shopping_behavior.csv)

## Workflow
| Stage | Tool | What was done |
|---|---|---|
| 1. Preparation | Python (pandas) | Imputed 37 missing review ratings with the category median, renamed columns to snake_case, created `age_group` (quartiles) and `purchase_frequency_days`, dropped `promo_code_used` (identical to `discount_applied`) |
| 2. Analysis | PostgreSQL | 10 business queries (revenue split, discounts, segments, rankings, window functions, CTEs) |
| 3. Visualization | Power BI | Interactive dashboard of customer behavior |

## 📓 Jupyter Notebook – Data Analysis

[💻 View Customer Shopping Behavior Analysis Notebook](https://github.com/bhor633/customer-shopping-behavior-analysis/blob/84e2f9d63a23457d4f2df22d191cbc4998c5172e/customer-shopping-behavior-analysis/customer-shopping-behavior-analysis/notebooks/customer_shopping_behavior.ipynb)

## Selected findings (from the SQL queries)
- **Total revenue:** $233,081 across 3,900 orders (average order $59.76).
- **Gender:** male customers generate $157,890 vs $75,191 from female customers (about 68% / 32%).
- **Subscription:** subscribers spend about the same per order ($59.49) as non-subscribers ($59.87), so subscription alone is not a spending driver in this data.
- **Shipping:** Express averages $60.48 vs $58.46 for Standard, a small gap.
- **Discounts:** 43% of purchases used a discount. Hats (50%) and Sneakers (49.7%) have the highest discount rates.
- **Top rated:** Gloves (3.86), Sandals (3.84), Boots (3.82).
- **Loyalty:** with the thresholds used (1 = New, 2-10 = Returning, 11+ = Loyal), 3,116 customers are Loyal, 701 Returning, 83 New.
- **Age:** the youngest quartile contributes the most revenue ($62,143); the other three quartiles are within about 10%.

- ## 🗄️ SQL Analysis & Queries

[💾 View SQL Queries – Customer Shopping Behavior Analysis](https://github.com/bhor633/customer-shopping-behavior-analysis/blob/84e2f9d63a23457d4f2df22d191cbc4998c5172e/customer-shopping-behavior-analysis/customer-shopping-behavior-analysis/sql/customer_shopping_behavior_sql_queries.sql)

## Recommendations
1. Review the discount strategy for Hats and Sneakers: half of their sales are discounted, so check whether margin is being given away on products that would sell anyway.
2. Redesign the subscription offer. It currently shows no spending uplift, so add benefits that raise basket size or frequency.
3. Investigate why female customers contribute far less revenue, using targeted campaigns or assortment changes.
4. Promote the best-rated products (Gloves, Sandals, Boots) in marketing.
5. Retain the large Loyal base with rewards, and look at how to bring in more new customers.

## Repository structure
```
├── data/raw/                 # original CSV
├── notebooks/                # exploratory cleaning notebook
├── scripts/data_preparation.py   # reproducible cleaning + optional DB load
├── sql/                      # 10 business queries
├── dashboard/                # Power BI (.pbix)
├── docs/                     # business problem document
└── images/                   # dashboard screenshots (add here)
```

## How to run
```bash
pip install -r requirements.txt
python scripts/data_preparation.py                    # writes data/processed/customer_cleaned.csv

# Optional: load into PostgreSQL (database must already exist)
export PG_PASSWORD=your_password
python scripts/data_preparation.py --load-db
```
Then run the queries in `sql/customer_shopping_behavior_sql_queries.sql` (table name: `customer`) and open `dashboard/customer_behavior_dashboard.pbix` in Power BI Desktop.

## Dashboard
<!-- Add a screenshot: images/dashboard.png -->

## 📊 Power BI Dashboard

[📄 View Customer Behavior Dashboard (PDF)](customer-shopping-behavior-analysis/customer-shopping-behavior-analysis/dashboard/customer_behavior_dashboard.pdf)

## Tech stack
Python, pandas, SQLAlchemy, PostgreSQL, Power BI

