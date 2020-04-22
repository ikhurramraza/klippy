import redis
import click

from pathlib import Path

from app.config import config


class Clipboard:
    STORE_KEY = f"klippy.{config.namespace()}"

    def __init__(self, config):
        self.config = config

    def copy(self, stream):
        pass

    def paste(self, stream):
        pass


class RedisClipboard(Clipboard):
    def __init__(self, config):
        super().__init__(config)
        self.conn = redis.Redis(**self.config, socket_connect_timeout=3)

    def copy(self, stream):
        try:
            self.conn.set(self.STORE_KEY, stream.read())
        except redis.exceptions.TimeoutError:
            click.ClickException('Connection timed out.').show()

    def paste(self, stream):
        try:
            stream.write(self.conn.get(self.STORE_KEY))
        except redis.exceptions.TimeoutError:
            click.ClickException('Connection timed out.').show()
