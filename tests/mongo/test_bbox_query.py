import requests
import pytest 
from random import randint

STAC_API_BASE_URL = "http://localhost:8083"

# COORDINATES = [[175.8, -82.84], [176.8, -82.84], [-176.0, -14.84], [-122.90, 35.21]]
COORDINATES = [[-69.433594,-10.660608,-47.285156,3.513421], [-129.684715,26.923811,-63.063621,51.850559]]
for x in range(1000):
    coord_1 = randint(-180, 0)
    coord_2 = randint(-90, 0)
    coord_3 = coord_1 + 15
    coord_4 = coord_2 + 15

    coordinates = [coord_1, coord_2, coord_3, coord_4]
    COORDINATES.append(coordinates)

@pytest.mark.parametrize('coordinates', COORDINATES)
def test_bbox_query(coordinates): 
    body = {
        "collections":["sentinel-s2-l2a-cogs"],
        "bbox":coordinates
    }
    resp = requests.post(f"{STAC_API_BASE_URL}/search", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert data["context"]["returned"] >= 1
