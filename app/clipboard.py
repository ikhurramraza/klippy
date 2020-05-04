import redis
import click

from pathlib import Path

from app.config import Settings


class Clipboard:
    STORE_KEY = f"klippy.{Settings.instance().namespace()}"

    __instance = None

    @classmethod
    def instance(cls):
        cls.__instance = cls.__instance or cls()
        return cls.__instance

    def copy(self, stream):
        pass

    def paste(self, stream):
        pass


class RedisClipboard(Clipboard):
    def __init__(self):
        self.conn = redis.Redis(**Settings.instance().redis(), socket_connect_timeout=3)

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
