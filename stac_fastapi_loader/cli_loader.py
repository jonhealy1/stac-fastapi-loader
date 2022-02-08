import click
import os
import json
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
STAC_API_BASE_URL = "http://localhost:8083"

def cli_message():
    click.secho()
    click.secho("""STAC FASTAPI LOADER""")

    click.secho("stac-fastapi-loader: Load STAC data into fastapi", bold=True)

    click.secho()

def load_data(filename):
    with open(os.path.join(DATA_DIR, filename)) as file:
        return json.load(file)

def load_collection():
    collection = load_data("test_collection.json")
    try:
        resp = requests.post(f"{STAC_API_BASE_URL}/collections", json=collection)
        click.secho(resp.status_code)
    except requests.ConnectionError:
        click.secho("failed to connect")

def load_item(collection):
    item = load_data("test_item.json")
    try:
        resp = requests.post(f"{STAC_API_BASE_URL}/collections/{collection}/items", json=collection)
        click.secho(resp.status_code)
    except requests.ConnectionError:
        click.secho("failed to connect")

# @click.option(
#     "-l", "--links", is_flag=True, help="Validate links for format and response."
# )
@click.command()
@click.argument('backend')
@click.version_option(version="0.1.4")
def main(backend):
    cli_message()
    load_item()