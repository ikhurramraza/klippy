import configparser
import os
from pathlib import Path


class Settings:
    PATH = f"{os.environ.get('XDG_CONFIG_HOME') or f'{Path.home()}/.config'}/klippy/config.ini"

    MAIN_DEFAULTS = {
        "namespace": "default",
    }

    REDIS_DEFAULTS = {
        "host": "127.0.0.1",
        "port": "6379",
        "password": "",
    }

    DEFAULTS = {
        "main": MAIN_DEFAULTS,
        "redis": REDIS_DEFAULTS,
    }

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.__load()

    def redis(self) -> dict[str, str]:
        return dict(self.config["redis"])

    def namespace(self) -> str:
        return self.config["main"]["namespace"]

    def set_namespace(self, namespace: str) -> None:
        self.config["main"]["namespace"] = namespace
        self.__save()

    def set_redis(self, host: str, port: str, password: str) -> None:
        self.config["redis"] = {"host": host, "port": port, "password": password}
        self.__save()

    def __save(self) -> None:
        Path(self.PATH).parent.mkdir(parents=True, exist_ok=True)
        with open(self.PATH, "w+") as configfile:
            self.config.write(configfile)

    def __load(self) -> None:
        for key, value in self.DEFAULTS.items():
            self.config.setdefault(key, value)

        self.config.read(self.PATH)
