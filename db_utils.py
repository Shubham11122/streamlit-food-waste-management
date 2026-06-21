"""
Data-access layer — thin wrappers around SQLite for CRUD operations.
All write helpers call conn.commit() and close the connection.
"""

import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = "food_wastage.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ─────────────────────────────────────────
# READ helpers
# ─────────────────────────────────────────

def read_sql(query: str, params: tuple = ()) -> pd.DataFrame:
    conn = get_conn()
    df   = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


# ─────────────────────────────────────────
# FOOD LISTINGS
# ─────────────────────────────────────────

def add_food(food_name, quantity, expiry_date, provider_id,
             location, food_type, meal_type):
    conn = get_conn()
    conn.execute("""
        INSERT INTO food_listings
            (food_name, quantity, expiry_date, provider_id, location, food_type, meal_type)
        VALUES (?,?,?,?,?,?,?)
    """, (food_name, quantity, str(expiry_date), provider_id,
          location, food_type, meal_type))
    conn.commit()
    conn.close()


def update_food(food_id, food_name, quantity, expiry_date,
                provider_id, location, food_type, meal_type):
    conn = get_conn()
    conn.execute("""
        UPDATE food_listings
        SET food_name=?, quantity=?, expiry_date=?,
            provider_id=?, location=?, food_type=?, meal_type=?
        WHERE food_id=?
    """, (food_name, quantity, str(expiry_date), provider_id,
          location, food_type, meal_type, food_id))
    conn.commit()
    conn.close()


def delete_food(food_id):
    conn = get_conn()
    conn.execute("DELETE FROM food_listings WHERE food_id=?", (food_id,))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────
# CLAIMS
# ─────────────────────────────────────────

def add_claim(food_id, receiver_id, status):
    conn = get_conn()
    conn.execute("""
        INSERT INTO claims (food_id, receiver_id, status, timestamp)
        VALUES (?,?,?,?)
    """, (food_id, receiver_id, status, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()


def update_claim(claim_id, status):
    conn = get_conn()
    conn.execute("UPDATE claims SET status=? WHERE claim_id=?", (status, claim_id))
    conn.commit()
    conn.close()


def delete_claim(claim_id):
    conn = get_conn()
    conn.execute("DELETE FROM claims WHERE claim_id=?", (claim_id,))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────
# PROVIDERS
# ─────────────────────────────────────────

def add_provider(name, ptype, address, city, contact):
    conn = get_conn()
    conn.execute("""
        INSERT INTO providers (name, type, address, city, contact)
        VALUES (?,?,?,?,?)
    """, (name, ptype, address, city, contact))
    conn.commit()
    conn.close()


def update_provider(provider_id, name, ptype, address, city, contact):
    conn = get_conn()
    conn.execute("""
        UPDATE providers
        SET name=?, type=?, address=?, city=?, contact=?
        WHERE provider_id=?
    """, (name, ptype, address, city, contact, provider_id))
    conn.commit()
    conn.close()


def delete_provider(provider_id):
    conn = get_conn()
    try:
        conn.execute("DELETE FROM providers WHERE provider_id=?", (provider_id,))
        conn.commit()
        return True, ""
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


# ─────────────────────────────────────────
# RECEIVERS
# ─────────────────────────────────────────

def add_receiver(name, rtype, city, contact):
    conn = get_conn()
    conn.execute("""
        INSERT INTO receivers (name, type, city, contact)
        VALUES (?,?,?,?)
    """, (name, rtype, city, contact))
    conn.commit()
    conn.close()


def update_receiver(receiver_id, name, rtype, city, contact):
    conn = get_conn()
    conn.execute("""
        UPDATE receivers
        SET name=?, type=?, city=?, contact=?
        WHERE receiver_id=?
    """, (name, rtype, city, contact, receiver_id))
    conn.commit()
    conn.close()


def delete_receiver(receiver_id):
    conn = get_conn()
    try:
        conn.execute("DELETE FROM receivers WHERE receiver_id=?", (receiver_id,))
        conn.commit()
        return True, ""
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()
