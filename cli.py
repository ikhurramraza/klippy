import click

from app.clipboard import RedisClipboard
from app.config import config
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
    clipboard = RedisClipboard(config.redis())
    clipboard.copy(file or click.get_binary_stream('stdin'))


@cli.command(help="Paste the data to file or stdout.")
@click.argument('file', required=False, type=click.File('wb'))
def paste(file):
    clipboard = RedisClipboard(config.redis())
    clipboard.paste(file or click.get_binary_stream('stdout'))


@cli.command(help=f"Configure settings file. ({config.PATH})")
def configure():
    namespace = click.prompt('Enter the name of namespace', default=config.namespace())
    host = click.prompt('Enter Redis host', default=config.redis().get('host'))
    port = click.prompt('Enter Redis port', default=config.redis().get('port'))
    password = click.prompt('Enter Redis password', default="")
    config.set_namespace(namespace)
    config.set_redis(host, port, password)
    config.save()


if __name__ == "__main__":
    cli()
