import click
import requests

def cli_message():
    click.secho()
    click.secho("""STAC FASTAPI LOADER""")

    click.secho("stac-fastapi-loader: Load STAC data into fastapi", bold=True)

    click.secho()

def load_item():
    try:
        r = requests.get("http://localhost:8083")
        print(r.status_code)
        print(r.content)
        # prints the int of the status code. Find more at httpstatusrappers.com :)
    except requests.ConnectionError:
        print("failed to connect")

# @click.option(
#     "-l", "--links", is_flag=True, help="Validate links for format and response."
# )
@click.command()
@click.argument('backend')
@click.version_option(version="0.1.4")
def main(backend):
    cli_message()
    load_item()