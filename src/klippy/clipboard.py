import click
import redis


class RedisClipboard:
    def __init__(self, settings):
        self.settings = settings
        self.conn = redis.Redis(**settings.redis(), socket_connect_timeout=3)

    def store_key(self):
        return f"klippy.{self.settings.namespace()}"

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
