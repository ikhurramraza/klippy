import configparser
from pathlib import Path


class Settings:
    PATH = f"{Path.home()}/.klippy.ini"

    MAIN_DEFAULTS = {
        'namespace': 'default',
    }

    REDIS_DEFAULTS = {
        'host': '127.0.0.1',
        'port': '6379',
        'password': '',
    }

    DEFAULTS = {
        'main': MAIN_DEFAULTS,
        'redis': REDIS_DEFAULTS,
    }

    __instance = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.__load()

    @classmethod
    def instance(cls):
        cls.__instance = cls.__instance or cls()
        return cls.__instance

    def redis(self):
        return dict(self.config['redis'])

    def namespace(self):
        return self.config['main']['namespace']

    def set_namespace(self, namespace):
        self.config['main']['namespace'] = namespace
        self.__save()

    def set_redis(self, host, port, password):
        self.config['redis'] = {'host': host, 'port': port, 'password': password}
        self.__save()

    def __save(self):
        with open(self.PATH, 'w+') as configfile:
            self.config.write(configfile)

    def __load(self):
        for key, value in self.DEFAULTS.items():
            self.config.setdefault(key, value)

        self.config.read(self.PATH)
