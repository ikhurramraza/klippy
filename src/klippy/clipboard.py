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
        self.conn.set(self.store_key(), stream.read())

    def paste(self, stream):
        data = self.conn.get(self.store_key())
        if data is not None:
            stream.write(data)
