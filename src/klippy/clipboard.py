import click
import redis

from klippy.config import Settings


class Clipboard:
    __instance = None

    @classmethod
    def instance(cls):
        cls.__instance = cls.__instance or cls()
        return cls.__instance

    def store_key(self):
        return f"klippy.{Settings.instance().namespace()}"

    def copy(self, stream):
        pass

    def paste(self, stream):
        pass

    def ping(self):
        pass


class RedisClipboard(Clipboard):
    def __init__(self):
        self.conn = redis.Redis(**Settings.instance().redis(), socket_connect_timeout=3)

    def ping(self):
        self.conn.ping()

    def copy(self, stream):
        try:
            self.conn.set(self.store_key(), stream.read())
        except redis.exceptions.TimeoutError:
            click.ClickException("Connection timed out.").show()

    def paste(self, stream):
        try:
            data = self.conn.get(self.store_key())
            if data is not None:
                stream.write(data)
        except redis.exceptions.TimeoutError:
            click.ClickException("Connection timed out.").show()
