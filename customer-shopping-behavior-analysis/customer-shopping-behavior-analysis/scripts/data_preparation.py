"""Clean the raw customer shopping dataset and (optionally) load it into PostgreSQL.

Usage:
    python scripts/data_preparation.py                 # writes data/processed/customer_cleaned.csv
    PG_PASSWORD=... python scripts/data_preparation.py --load-db
"""
import argparse
import os
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "customer_shopping_behavior.csv"
OUT = ROOT / "data" / "processed" / "customer_cleaned.csv"

FREQUENCY_DAYS = {
    "Weekly": 7, "Fortnightly": 14, "Bi-Weekly": 14, "Monthly": 30,
    "Quarterly": 90, "Every 3 Months": 90, "Annually": 365,
}


def clean(df: pd.DataFrame) -> pd.DataFrame:
    # Impute missing review ratings with the median of the product category
    df["Review Rating"] = df.groupby("Category")["Review Rating"].transform(
        lambda x: x.fillna(x.median())
    )

    # snake_case column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df = df.rename(columns={"purchase_amount_(usd)": "purchase_amount"})

    # Feature engineering
    df["age_group"] = pd.qcut(
        df["age"], q=4, labels=["Young Adult", "Adult", "Middle-aged", "Senior"]
    )
    df["purchase_frequency_days"] = df["frequency_of_purchases"].map(FREQUENCY_DAYS)

    # discount_applied and promo_code_used are identical -> drop the redundant one
    if (df["discount_applied"] == df["promo_code_used"]).all():
        df = df.drop(columns="promo_code_used")
    return df


def load_to_postgres(df: pd.DataFrame) -> None:
    from sqlalchemy import create_engine

    url = "postgresql+psycopg2://{u}:{p}@{h}:{port}/{d}".format(
        u=os.getenv("PG_USER", "postgres"),
        p=os.environ["PG_PASSWORD"],
        h=os.getenv("PG_HOST", "localhost"),
        port=os.getenv("PG_PORT", "5432"),
        d=os.getenv("PG_DB", "customer_shopping_behavior"),
    )
    df.to_sql("customer", create_engine(url), if_exists="replace", index=False)
    print("Loaded table 'customer' into PostgreSQL.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--load-db", action="store_true", help="also load into PostgreSQL")
    args = parser.parse_args()

    data = clean(pd.read_csv(RAW, encoding="utf-8-sig"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUT, index=False)
    print(f"Cleaned data: {data.shape[0]} rows x {data.shape[1]} cols -> {OUT}")
    if args.load_db:
        load_to_postgres(data)
