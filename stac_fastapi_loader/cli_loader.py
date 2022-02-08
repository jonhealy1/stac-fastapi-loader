import click


def cli_message():
    click.secho()
    click.secho("""STAC FASTAPI LOADER""")

    click.secho("stac-fastapi-loader: Load STAC data into fastapi", bold=True)

    click.secho()

# @click.option(
#     "-l", "--links", is_flag=True, help="Validate links for format and response."
# )
@click.command()
@click.argument('backend')
@click.version_option(version="0.1.4")
def main(backend):
    cli_message()