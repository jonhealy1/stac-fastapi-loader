import requests
import pytest 

STAC_API_BASE_URL = "http://localhost:8083"

COORDINATES = [[175.8, -82.84], [176.8, -82.84]]

@pytest.mark.parametrize('coordinates', COORDINATES)
def test_point_query(coordinates): 
    body = {
        "collections":["sentinel-s2-l2a-cogs"],
        "intersects":{"type": "Point", "coordinates": coordinates}
    }
    resp = requests.post(f"{STAC_API_BASE_URL}/search", json=body)
    data = resp.json()
    assert data["context"]["returned"] >= 10
