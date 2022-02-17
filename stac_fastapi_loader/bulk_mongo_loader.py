import pymongo
import json
import os
from pymongo import MongoClient, errors

DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data/sentinel_data")

def load_file(filename: str):
    with open(os.path.join(DATA_DIR, filename)) as file:
        return json.load(file)

def unordered_bulk_write():
    client = create_client()
    item_table = client.stac.stac_item
    bulk_op = item_table.initialize_unordered_bulk_op()

    file = load_file("sentinel-s2-l2a-cogs_180001_210000.json")
    # for primary_key in file[""]:
    #     bulk_op.find({'fubar_key': primary_key}).update({'$set': {'dopeness_factor': 'unlimited'}})

    # try:
    #     bulk_op.execute()
    for feature in file["features"]:
        feature["stac_extensions"] = []
        feature["stac_version"] = "1.0.0"

    with client.start_session(causal_consistency=True) as session:
        item_table.insert_many(file["features"], session=session)

def create_client():
    """Create mongo client."""
    try:
        client = MongoClient(
            host=["localhost" + ":" + str(27017)],
            serverSelectionTimeoutMS=3000,
            username="dev",
            password="stac",
        )

        # create indices - they are only created if they don't already exist
        # item_table = client.stac.stac_item
        # item_table.create_index([("bbox", GEOSPHERE), ("properties.datetime", 1)])
        # item_table.create_index([("geometry", GEOSPHERE)])
        # item_table.create_index([("properties.datetime", 1)])
        # item_table.create_index([("properties.created", 1)])
        # item_table.create_index([("properties.updated", 1)])
        # item_table.create_index([("bbox", GEOSPHERE)])
        # item_table.create_index([("bbox", GEO2D)])

    except errors.ServerSelectionTimeoutError as err:
        client = None
        print("pymongo ERROR:", err)

    return client

print("hello")
unordered_bulk_write()