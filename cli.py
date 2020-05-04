import click

from app.clipboard import RedisClipboard
from app.config import Settings
from app.version import VERSION


@click.group()
@click.version_option(VERSION)
def cli():
    """A command line utility that acts like a cloud clipboard.

    Good to know: A single Redis server can be shared among different people
    or you can have multiple clipboards by using different namespaces.
    """
    pass


@cli.command(help="Copy the data from file or stdin.")
@click.argument('file', required=False, type=click.File('rb'))
def copy(file):
    RedisClipboard.instance().copy(file or click.get_binary_stream('stdin'))


@cli.command(help="Paste the data to file or stdout.")
@click.argument('file', required=False, type=click.File('wb'))
def paste(file):
    RedisClipboard.instance().paste(file or click.get_binary_stream('stdout'))


@cli.command(help=f"Configure settings file. ({Settings.PATH})")
def configure():
    namespace = click.prompt('Enter the name of namespace', default=Settings.instance().namespace())
    host = click.prompt('Enter Redis host', default=Settings.instance().redis().get('host'))
    port = click.prompt('Enter Redis port', default=Settings.instance().redis().get('port'))
    password = click.prompt('Enter Redis password', default="")
    Settings.instance().set_namespace(namespace)
    Settings.instance().set_redis(host, port, password)


if __name__ == "__main__":
    cli()
