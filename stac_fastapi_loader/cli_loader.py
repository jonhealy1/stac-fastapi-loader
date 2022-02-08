import click


def cli_message():
    click.secho("""
 ____  ____  __    ___       ___  _  _  ____  ___  __ _ 
/ ___)(_  _)/ _\  / __)___  / __)/ )( \(  __)/ __)(  / )
\___ \  )( /    \( (__(___)( (__ ) __ ( ) _)( (__  )  ( 
(____/ (__)\_/\_/ \___)     \___)\_)(_/(____)\___)(__\_)
    """)

    click.secho("stac-check: STAC spec validaton and linting tool", bold=True)

    click.secho()

@click.option(
    "-r", "--recursive", is_flag=True, help="Validate all assets in a collection or catalog."
)
@click.option(
    "-a", "--assets", is_flag=True, help="Validate assets for format and response."
)
@click.option(
    "-l", "--links", is_flag=True, help="Validate links for format and response."
)
@click.command()
@click.argument('file')
@click.version_option(version="0.1.4")
def main(file, assets, links, recursive):
    cli_message()