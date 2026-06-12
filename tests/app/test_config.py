import os
import shutil
import unittest

from app.config import Settings


class TestConfig(unittest.TestCase):
    TEMP_CONFIG_PATH = "tests/.tmp/config.ini"
    TEMP_LEGACY_CONFIG_PATH = "tests/.tmp.legacy.ini"

    def setUp(self):
        Settings.PATH = self.TEMP_CONFIG_PATH
        Settings.LEGACY_PATH = self.TEMP_LEGACY_CONFIG_PATH
        self.subject = Settings()

    def tearDown(self):
        if os.path.exists(Settings.LEGACY_PATH):
            os.remove(Settings.LEGACY_PATH)
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

    def test_migrates_legacy_config(self):
        with open(self.TEMP_LEGACY_CONFIG_PATH, "w") as legacy_file:
            legacy_file.write("[main]\nnamespace = legacy_namespace\n")

        subject = Settings()
        self.assertEqual("legacy_namespace", subject.namespace())
        self.assertTrue(os.path.exists(self.TEMP_CONFIG_PATH))
        self.assertFalse(os.path.exists(self.TEMP_LEGACY_CONFIG_PATH))

    def test_does_not_migrate_when_config_exists(self):
        self.subject.set_namespace("current_namespace")
        with open(self.TEMP_LEGACY_CONFIG_PATH, "w") as legacy_file:
            legacy_file.write("[main]\nnamespace = legacy_namespace\n")

        subject = Settings()
        self.assertEqual("current_namespace", subject.namespace())
        self.assertTrue(os.path.exists(self.TEMP_LEGACY_CONFIG_PATH))
