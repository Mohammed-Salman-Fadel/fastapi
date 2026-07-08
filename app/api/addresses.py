from fastapi import FastAPI, HTTPException
import sqlite3
from app.schema.address import AddressCreate, AddressResponse
from typing import List
from main import app

conn = sqlite3.connect("app/db/addresses.db", check_same_thread=False)
conn.row_factory = sqlite3.Row


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

create_table()

@app.get('/addresses/{address_id}', response_model=AddressResponse)
def get_address(address_id: int):
    cur = conn.cursor()

    cur.execute("SELECT * FROM addresses WHERE id = ?", (address_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return dict(row)

@app.get('/addresses/', response_model=List[AddressResponse])
def get_all_address():
    with conn:
        cur = conn.cursor()

        rows = cur.execute("SELECT * FROM addresses").fetchall()
    return [dict(row) for row in rows]

@app.post('/addresses/', response_model=AddressResponse)
def add_address(address: AddressCreate):
    with conn:
        cur = conn.cursor()

        cur.execute("INSERT INTO addresses (street, city, country, postal_code, longitude, latitude) VALUES (?,?,?,?,?,?)",
                (address.street, address.city, address.country, address.postal_code, address.longitude, address.latitude))

        last_row_id = cur.lastrowid
        row = cur.execute("SELECT * FROM addresses WHERE id = ?", (last_row_id,)).fetchone()
        
    return dict(row)

@app.delete('/addresses/{address_id}', response_model=AddressResponse)
def delete_address(address_id: int):
    with conn:
        cur = conn.cursor()
        
        row = cur.execute("SELECT * FROM addresses WHERE id = ?", (address_id,)).fetchone()
        
        if row is None:
            raise HTTPException(status_code=404, detail="Address ID does not exist.")
        cur.execute("DELETE FROM addresses WHERE id = ?", (address_id,))
        
    return dict(row)