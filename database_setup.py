"""
Run this once to build food_wastage.db from the CSV files in data/
    python database_setup.py
"""

import pandas as pd
import sqlite3
import os

DATA_DIR = "data"
DB_PATH  = "food_wastage.db"

def build_database():
    providers = pd.read_csv(os.path.join(DATA_DIR, "providers_data.csv"))
    receivers = pd.read_csv(os.path.join(DATA_DIR, "receivers_data.csv"))
    food      = pd.read_csv(os.path.join(DATA_DIR, "food_listings_data.csv"))
    claims    = pd.read_csv(os.path.join(DATA_DIR, "claims_data.csv"))

    for df in [providers, receivers, food, claims]:
        df.columns = [c.lower() for c in df.columns]

    conn = sqlite3.connect(DB_PATH)

    providers.to_sql("providers",     conn, if_exists="replace", index=False)
    receivers.to_sql("receivers",     conn, if_exists="replace", index=False)
    food.to_sql("food_listings",      conn, if_exists="replace", index=False)
    claims.to_sql("claims",           conn, if_exists="replace", index=False)

    conn.close()
    print(f"✅ {DB_PATH} created successfully")

if __name__ == "__main__":
    build_database()
