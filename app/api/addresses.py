from fastapi import APIRouter, HTTPException
from app.schema.address import AddressCreate, AddressResponse
from app.db.database import create_table
from app.db.database import conn
from typing import List
import logging
from app.api.formula import haversine_distance

router = APIRouter()

logger = logging.getLogger(__name__)

create_table()



@router.get('/addresses/', response_model=List[AddressResponse], tags=["GET Address"])
def get_all_address():
    """
    GET method to return all addresses in the SQLite database.
    """
    logger.info("Fetching all addresses")
    
    cur = conn.cursor()

    rows = cur.execute("SELECT * FROM addresses").fetchall()
    if not rows:
        logger.warning("No addresses found in database")
        raise HTTPException(status_code=404, detail="No addresses found.")
    
    logger.info(f"Retrieved {len(rows)} addresses")
    return [dict(row) for row in rows]

@router.get('/addresses/coordinates', response_model=AddressResponse,  tags=["GET Address"])
def get_address_by_coordinates(longitude: float, latitude: float):
    """
    GET method to return an address given its exact latitude and longitude.
    """
    logger.info(f"Fetching address with lat={latitude}, lon={longitude}")

    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM addresses WHERE latitude = ? AND longitude = ?", (latitude, longitude)
    )
    row = cur.fetchone()

    if not row:
        logger.warning(f"Address not found for lat={latitude}, lon={longitude}")
        raise HTTPException(status_code=404, detail="Address not found.")

    logger.info(f"Address found for lat={latitude}, lon={longitude}")
    return dict(row)

@router.get('/addresses/nearby', response_model=List[AddressResponse],  tags=["GET Address"])
def get_nearby_addresses(longitude: float, latitude: float, radius_km: float = 5):
    """
    GET method to compute if the address are "nearby" the user's input.
    
    The user enters the radius and the addresses within that radius will be returned.
    
    Radius value is default = 5 km.
    """
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM addresses").fetchall()

    nearby = []
    for row in rows:
        row = dict(row)
        distance = haversine_distance(latitude, longitude, row["latitude"], row["longitude"])
        if distance <= radius_km:
            nearby.append(row)
    
    if not nearby:
        logger.info(f"No addresses within {radius_km} km distance")
        HTTPException(status_code=404, detail=f"No address within {radius_km}km radius.")

    return nearby

@router.get('/addresses/{address_id}', response_model=AddressResponse,  tags=["GET Address"])
def get_address(address_id: int):
    """
    GET method to return an address given the address ID.
    """
    logger.info(f"Fetching address with id={address_id}")
    
    cur = conn.cursor()

    cur.execute("SELECT * FROM addresses WHERE id = ?", (address_id,))
    row = cur.fetchone()
    if not row:
        logger.warning(f"Address not found: id={address_id}")
        raise HTTPException(status_code=404, detail="Address not found.")
    
    logger.info(f"Address found: id={address_id}")
    return dict(row)

@router.post('/addresses/', response_model=AddressResponse, tags=["POST Address"])
def add_address(address: AddressCreate):
    """
    POST method to add an address given the AddressCreate model.
    """
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
        
        # Select the last row id to return the last added item into the table
        last_row_id = cur.lastrowid
        row = cur.execute("SELECT * FROM addresses WHERE id = ?", (last_row_id,)).fetchone()
    
    logger.info(f"Address created successfully: id={last_row_id}")
    return dict(row)

@router.delete('/addresses/{address_id}', response_model=AddressResponse, tags=["DELETE Address"])
def delete_address(address_id: int):
    """
    DEL method to delete an address given the address ID.
    """
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


@router.put('/addresses/{address_id}', response_model=AddressResponse, tags=["UPDATE Address"])
def update_address(address_id: int, address: AddressCreate):
    """
    PUT method to update an existing address given the address ID.
    """
    logger.info(f"Attempting to update address id={address_id}")
    with conn:
        cur = conn.cursor()

        # Check if the address exists
        existing = cur.execute("SELECT * FROM addresses WHERE id = ?", (address_id,)).fetchone()
        
        if not existing:
            logger.warning(f"Update failed, address not found: id={address_id}")
            raise HTTPException(status_code=404, detail="Address was not found.")

        # Check if the latitude is unique
        existing_lat = cur.execute("SELECT id FROM addresses WHERE latitude = ? AND id != ?", (address.latitude, address_id)).fetchone()
        
        if existing_lat:
            logger.warning(f"Duplicate latitude rejected: {address.latitude}")
            raise HTTPException(
                status_code=404,
                detail=f"An address with latitude {address.latitude} already exists."
            )

        # Check if the longitude is unique
        existing_lon = cur.execute("SELECT id FROM addresses WHERE longitude = ? AND id != ?", (address.longitude, address_id)).fetchone()
        
        if existing_lon:
            logger.warning(f"Duplicate longitude rejected: {address.longitude}")
            raise HTTPException(
                status_code=404,
                detail=f"An address with longitude {address.longitude} already exists."
            )

        cur.execute("""
            UPDATE addresses
            SET street = ?, city = ?, country = ?, postal_code = ?, longitude = ?, latitude = ? WHERE id = ?""",
                (address.street, address.city, address.country, address.postal_code,
                address.longitude, address.latitude, address_id))

        row = cur.execute("SELECT * FROM addresses WHERE id = ?", (address_id,)).fetchone()

    logger.info(f"Address updated successfully: id={address_id}")
    return dict(row)