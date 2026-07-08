from pydantic import BaseModel

# Pydantic Models - Defines structure to return/create. 
class AddressCreate(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str
    longitude: float
    latitude: float

class AddressResponse(BaseModel):
    id: int
    street: str
    city: str
    country: str
    postal_code: str
    longitude: float
    latitude: float