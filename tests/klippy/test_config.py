import os
import shutil
import unittest

from klippy.config import Settings


class TestConfig(unittest.TestCase):
    TEMP_CONFIG_PATH = "tests/.tmp/config.ini"

    def setUp(self):
        Settings.PATH = self.TEMP_CONFIG_PATH
        self.subject = Settings()

    def tearDown(self):
        shutil.rmtree("tests/.tmp", ignore_errors=True)

    def test_defaults(self):
        expected_namespace = "default"
        expected_redis = {"host": "127.0.0.1", "port": "6379", "password": ""}
        self.assertEqual(expected_namespace, self.subject.namespace())
        self.assertEqual(expected_redis, self.subject.redis())

    def test_set_namespace(self):
        self.subject.set_namespace("test")
        self.assertEqual("test", self.subject.namespace())

    def test_set_redis(self):
        self.subject.set_redis("test.klippy", "12345", "secret")
        expected = {"host": "test.klippy", "port": "12345", "password": "secret"}
        self.assertEqual(expected, self.subject.redis())

    def test_save_creates_parent_directories(self):
        self.subject.set_namespace("test")
        self.assertTrue(os.path.exists(self.TEMP_CONFIG_PATH))
