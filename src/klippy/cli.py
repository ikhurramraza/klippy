import os

import click
import redis

from klippy.clipboard import RedisClipboard
from klippy.config import Settings
from klippy.version import VERSION


@click.group()
@click.version_option(VERSION)
def cli():
    """A command line utility that acts like a cloud clipboard.

    Good to know: A single Redis server can be shared among different people
    or you can have multiple clipboards by using different namespaces.
    """
    pass


@cli.command(help="Copy the data from file or stdin.")
@click.argument("file", required=False, type=click.File("rb"))
def copy(file):
    RedisClipboard.instance().copy(file or click.get_binary_stream("stdin"))


@cli.command(help="Paste the data to file or stdout.")
@click.argument("file", required=False, type=click.File("wb"))
def paste(file):
    RedisClipboard.instance().paste(file or click.get_binary_stream("stdout"))


@cli.command(help=f"Configure settings file. ({Settings.PATH})")
def configure():
    namespace = click.prompt("Enter the name of namespace", default=Settings.instance().namespace())
    host = click.prompt("Enter Redis host", default=Settings.instance().redis().get("host"))
    port = click.prompt("Enter Redis port", default=Settings.instance().redis().get("port"))
    password = click.prompt("Enter Redis password", default="")
    Settings.instance().set_namespace(namespace)
    Settings.instance().set_redis(host, port, password)


@cli.command(help="Check the configuration and the connection to the Redis server.")
def doctor():
    config_status = "found" if os.path.exists(Settings.PATH) else "not found, using defaults"
    click.echo(f"Settings file: {Settings.PATH} ({config_status})")
    click.echo(f"Namespace: {Settings.instance().namespace()}")

    redis_settings = Settings.instance().redis()
    click.echo(f"Redis server: {redis_settings['host']}:{redis_settings['port']}")

    try:
        RedisClipboard.instance().ping()
    except redis.exceptions.RedisError as error:
        raise click.ClickException(f"Connection failed. ({error})")

    click.secho("Connection: OK", fg="green")


if __name__ == "__main__":
    cli()
