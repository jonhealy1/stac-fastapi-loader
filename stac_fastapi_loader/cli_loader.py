import click
import os
import json
import requests

from stac_fastapi_loader.bulk_mongo_loader import bulk_write

DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data/sentinel_data")
# STAC_API_BASE_URL = "http://localhost:8083"

def cli_message():
    click.secho()
    click.secho("""STAC FASTAPI LOADER""")

    click.secho("stac-fastapi-loader: Load STAC data into fastapi", bold=True)

    click.secho()

def load_data(filename):
    with open(os.path.join(DATA_DIR, filename)) as file:
        return json.load(file)

def load_collection(base_url, collection_id):
    data_dir = os.path.join(os.path.dirname(__file__), "test_data")
    with open(os.path.join(data_dir, "test_collection.json")) as file:
        collection = json.load(file)
    collection["id"] = collection_id
    try:
        resp = requests.post(f"{base_url}/collections", json=collection)
    except requests.ConnectionError:
        click.secho("failed to connect")

def load_items(base_url):
    feature_collections = []
    for filename in os.listdir(DATA_DIR):
        item = load_data(filename)
        feature_collections.append(item)
        print(filename)

    collection = item["features"][0]["collection"]
    load_collection(base_url, collection)
    
    for items in feature_collections: 
        for feature in items["features"]:
            try:
                feature["stac_extensions"] = []
                feature["stac_version"] = "1.0.0"
                resp = requests.post(f"{base_url}/collections/{collection}/items", json=feature)
            except requests.ConnectionError:
                click.secho("failed to connect")

def load_item(base_url, filename):
    print(filename)
    feature_collection = load_data(str(filename))
    collection = feature_collection["features"][0]["collection"]
    load_collection(base_url, collection)
    for feature in feature_collection["features"]: 
        try:
            feature["stac_extensions"] = []
            feature["stac_version"] = "1.0.0"
            resp = requests.post(f"{base_url}/collections/{collection}/items", json=feature)
        except requests.ConnectionError:
            click.secho("failed to connect")

@click.option(
    "--bulk", is_flag=True, help="Bulk load items"
)
@click.option(
    "--folder", is_flag=True, help="Load all items in sentinel_data folder"
)
@click.option(
    "--file",
    help="Load one specified file",
)
@click.command()
@click.argument('backend')
@click.version_option(version="0.1.4")
def main(backend, bulk, file, folder):
    cli_message()
    base_url = ""
    if backend == 'mongo':
        base_url = "http://localhost:8083"
    elif backend == 'elasticsearch':
        base_url = "http://localhost:8083"
    if folder:
        load_items(base_url)
    if file:
        load_item(base_url, file)
    if bulk and backend == 'mongo':
        bulk_write()
