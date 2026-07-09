import sqlite3
from app.core.config import config

conn = sqlite3.connect(f"app/db/{config.db_name}", check_same_thread=False)
conn.row_factory = sqlite3.Row

# Addresses table definition
def create_table():
    cur = conn.cursor()
    
    with conn:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS addresses(
                    id INTEGER PRIMARY KEY,
                    street TEXT CHECK(length(street) <= 100),
                    city TEXT CHECK(length(street) <= 100),
                    country TEXT CHECK(length(street) <= 100),
                    postal_code TEXT CHECK(length(street) <= 20),
                    longitude REAL UNIQUE,
                    latitude REAL UNIQUE
                    )
                """)


def sample_create():
    cur = conn.cursor()
    sample_addresses = [
                        ("Roxas Boulevard", "Manila", "Philippines","1000", 120.979683, 14.582919),
                        ("Santa Clara Street", "Manila", "Philippines","1002", 120.970100, 14.594200),
                        ("Gelen Dost Street", "Ankara", "Turkey", "06300", 120.982200, 14.535100)
                        ]
    
    with conn:
        cur.executemany("INSERT INTO addresses (street, city, country, postal_code, longitude, latitude) VALUES (?,?,?,?,?,?)", sample_addresses)

# sample_create()