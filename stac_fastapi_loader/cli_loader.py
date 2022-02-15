import click
import os
import json
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data/sentinel_data")
STAC_API_BASE_URL = "http://localhost:8083"

def cli_message():
    click.secho()
    click.secho("""STAC FASTAPI LOADER""")

    click.secho("stac-fastapi-loader: Load STAC data into fastapi", bold=True)

    click.secho()

def load_data(filename):
    with open(os.path.join(DATA_DIR, filename)) as file:
        return json.load(file)

def load_collection(collection_id):
    data_dir = os.path.join(os.path.dirname(__file__), "test_data")
    with open(os.path.join(data_dir, "test_collection.json")) as file:
        collection = json.load(file)
    collection["id"] = collection_id
    try:
        resp = requests.post(f"{STAC_API_BASE_URL}/collections", json=collection)
    except requests.ConnectionError:
        click.secho("failed to connect")

def load_items():
    feature_collections = []
    for filename in os.listdir(DATA_DIR):
        item = load_data(filename)
        feature_collections.append(item)
        print(filename)

    collection = item["features"][0]["collection"]
    load_collection(collection)
    
    for items in feature_collections: 
        for feature in items["features"]:
            try:
                feature["stac_extensions"] = []
                feature["stac_version"] = "1.0.0"
                resp = requests.post(f"{STAC_API_BASE_URL}/collections/{collection}/items", json=feature)
            except requests.ConnectionError:
                click.secho("failed to connect")

def load_item(filename):
    print(filename)
    feature_collection = load_data(str(filename))
    collection = feature_collection["features"][0]["collection"]
    print(collection)
    load_collection(collection)
    for feature in feature_collection["features"]: 
        print(feature)
        try:
            feature["stac_extensions"] = []
            feature["stac_version"] = "1.0.0"
            resp = requests.post(f"{STAC_API_BASE_URL}/collections/{collection}/items", json=feature)
        except requests.ConnectionError:
            click.secho("failed to connect")

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
def main(backend, file, folder):
    cli_message()
    if folder:
        load_items()
    if file:
        load_item(file)