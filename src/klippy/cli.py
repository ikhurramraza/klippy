import os
import re

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


def parse_duration(ctx, param, value):
    if value is None:
        return None

    match = re.fullmatch(r"(\d+)([smhd])", value)
    if not match:
        raise click.BadParameter("expected a number followed by a unit, e.g. 90s, 5m, 2h, 1d")

    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    seconds = int(match.group(1)) * seconds_per_unit[match.group(2)]
    if seconds == 0:
        raise click.BadParameter("duration must be greater than zero")

    return seconds


@cli.command(help="Copy the data from file or stdin.")
@click.argument("file", required=False, type=click.File("rb"))
@click.option(
    "--expire",
    "-e",
    callback=parse_duration,
    help="Expire the clip after a duration, e.g. 90s, 5m, 2h, 1d.",
)
def copy(file, expire):
    try:
        RedisClipboard(Settings()).copy(file or click.get_binary_stream("stdin"), expire=expire)
    except redis.exceptions.RedisError as error:
        raise click.ClickException(f"Copy failed, try 'klippy doctor'. ({error})")


@cli.command(help="Paste the data to file or stdout.")
@click.argument("file", required=False, type=click.File("wb"))
def paste(file):
    try:
        RedisClipboard(Settings()).paste(file or click.get_binary_stream("stdout"))
    except redis.exceptions.RedisError as error:
        raise click.ClickException(f"Paste failed, try 'klippy doctor'. ({error})")


@cli.command(help="Clear the clipboard.")
def clear():
    try:
        RedisClipboard(Settings()).clear()
    except redis.exceptions.RedisError as error:
        raise click.ClickException(f"Clear failed, try 'klippy doctor'. ({error})")
    click.echo("Clipboard cleared.")


@cli.command(help=f"Configure settings file. ({Settings.PATH})")
def configure():
    settings = Settings()
    namespace = click.prompt("Enter the name of namespace", default=settings.namespace())
    host = click.prompt("Enter Redis host", default=settings.redis().get("host"))
    port = click.prompt("Enter Redis port", default=settings.redis().get("port"))
    password = click.prompt(
        "Enter Redis password",
        default=settings.redis().get("password", ""),
        hide_input=True,
        show_default=False,
    )
    settings.set_namespace(namespace)
    settings.set_redis(host, port, password)


@cli.command(help="Check the configuration and the connection to the Redis server.")
def doctor():
    settings = Settings()

    config_status = "found" if os.path.exists(Settings.PATH) else "not found, using defaults"
    click.echo(f"Settings file: {Settings.PATH} ({config_status})")
    click.echo(f"Namespace: {settings.namespace()}")

    redis_settings = settings.redis()
    click.echo(f"Redis server: {redis_settings['host']}:{redis_settings['port']}")

    try:
        RedisClipboard(settings).ping()
    except redis.exceptions.RedisError as error:
        raise click.ClickException(f"Connection failed. ({error})")

    click.secho("Connection: OK", fg="green")


if __name__ == "__main__":
    cli()
