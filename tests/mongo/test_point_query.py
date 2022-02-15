import requests

STAC_API_BASE_URL = "http://localhost:8083"

def test_point_query():
    body = {
        "collections":["sentinel-s2-l2a-cogs"],
        "intersects":{"type": "Point", "coordinates": [175.8, -82.84]}
    }
    resp = requests.post(f"{STAC_API_BASE_URL}/search", json=body)
    data = resp.json()
    assert data["context"]["returned"] >= 10
