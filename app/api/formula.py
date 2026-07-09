from math import radians, sin, cos, sqrt, atan2

"""
From my searching, the Haversine formula is the most suitable formula for determining 
the distance between two points on a sphere like object.

I copied the formula below to be used to get the addresses within a 5km radius from
the user's GET request.
"""

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    R = 6371  # Earth's radius in kilometers

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  # Returns distance in kilometers