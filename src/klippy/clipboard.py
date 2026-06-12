from typing import BinaryIO

import redis

from klippy.config import Settings


class RedisClipboard:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.conn = redis.Redis(**settings.redis(), socket_connect_timeout=3)

    def store_key(self) -> str:
        return f"klippy.{self.settings.namespace()}"

    def ping(self) -> None:
        self.conn.ping()

    def copy(self, stream: BinaryIO, expire: int | None = None) -> None:
        self.conn.set(self.store_key(), stream.read(), ex=expire)

    def paste(self, stream: BinaryIO) -> None:
        data = self.conn.get(self.store_key())
        if data is not None:
            stream.write(data)

    def clear(self) -> None:
        self.conn.delete(self.store_key())
