from fastapi import APIRouter, HTTPException
from app.schema.address import AddressCreate, AddressResponse
from app.db.database import create_table
from app.db.database import conn
from typing import List
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

create_table()

@router.get('/addresses/{address_id}', response_model=AddressResponse)
def get_address(address_id: int):
    logger.info(f"Fetching address with id={address_id}")
    
    cur = conn.cursor()

    cur.execute("SELECT * FROM addresses WHERE id = ?", (address_id,))
    row = cur.fetchone()
    if not row:
        logger.warning(f"Address not found: id={address_id}")
        raise HTTPException(status_code=404, detail="Address not found.")
    
    logger.info(f"Address found: id={address_id}")
    return dict(row)

@router.get('/addresses/', response_model=List[AddressResponse])
def get_all_address():
    logger.info("Fetching all addresses")
    
    cur = conn.cursor()

    rows = cur.execute("SELECT * FROM addresses").fetchall()
    if not rows:
        logger.warning("No addresses found in database")
        raise HTTPException(status_code=404, detail="No addresses found.")
    
    logger.info(f"Retrieved {len(rows)} addresses")
    return [dict(row) for row in rows]

@router.post('/addresses/', response_model=AddressResponse)
def add_address(address: AddressCreate):
    logger.info(f"Attempting to add address: lat={address.latitude}, lon={address.longitude}")
    with conn:
        cur = conn.cursor()

        # Check latitude uniqueness
        existing_lat = cur.execute(
            "SELECT id FROM addresses WHERE latitude = ?", (address.latitude,)
        ).fetchone()
        if existing_lat:
            logger.warning(f"Duplicate latitude rejected: {address.longitude}")
            raise HTTPException(
                status_code=404,
                detail=f"An address with latitude {address.latitude} already exists."
            )

        # Check longitude uniqueness
        existing_lon = cur.execute(
            "SELECT id FROM addresses WHERE longitude = ?", (address.longitude,)
        ).fetchone()
        if existing_lon:
            logger.warning(f"Duplicate longitude rejected: {address.longitude}")
            raise HTTPException(
                status_code=404,
                detail=f"An address with longitude {address.longitude} already exists."
            )
        
        cur.execute("INSERT INTO addresses (street, city, country, postal_code, longitude, latitude) VALUES (?,?,?,?,?,?)",
                (address.street, address.city, address.country, address.postal_code, address.longitude, address.latitude))

        last_row_id = cur.lastrowid
        row = cur.execute("SELECT * FROM addresses WHERE id = ?", (last_row_id,)).fetchone()
    
    logger.info(f"Address created successfully: id={last_row_id}")
    return dict(row)

@router.delete('/addresses/{address_id}', response_model=AddressResponse)
def delete_address(address_id: int):
    logger.info(f"Attempting to delete address id={address_id}")
    with conn:
        cur = conn.cursor()
        
        row = cur.execute("SELECT * FROM addresses WHERE id = ?", (address_id,)).fetchone()
        
        if not row:
            logger.warning(f"Delete failed, address not found: id={address_id}")
            raise HTTPException(status_code=404, detail="Address was not found.")
        
        cur.execute("DELETE FROM addresses WHERE id = ?", (address_id,))
    
    logger.info(f"Address deleted successfully: id={address_id}")
    return dict(row)