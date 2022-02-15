import requests
import pytest 
from random import randint

STAC_API_BASE_URL = "http://localhost:8083"

COORDINATES = [[175.8, -82.84], [176.8, -82.84], [-176.0, -14.84]]

for x in range(10000):
    coord_1 = randint(-180, 180)
    coord_2 = randint(-90, 90)
    coordinates = [coord_1, coord_2]
    COORDINATES.append(coordinates)

@pytest.mark.parametrize('coordinates', COORDINATES)
def test_point_query(coordinates): 
    body = {
        "collections":["sentinel-s2-l2a-cogs"],
        "intersects":{"type": "Point", "coordinates": coordinates}
    }
    resp = requests.post(f"{STAC_API_BASE_URL}/search", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert data["context"]["returned"] >= 1
