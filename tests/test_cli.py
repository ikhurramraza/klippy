import os

import unittest
import fakeredis
from click.testing import CliRunner

import cli
from app.config import Settings
from app.clipboard import RedisClipboard


class TestCliConfigure(unittest.TestCase):
    TEMP_CONFIG_PATH = 'tests/.tmp.ini'

    def setUp(self):
        Settings.PATH = self.TEMP_CONFIG_PATH
        self.__run_with_sample_prompt_value()

    def tearDown(self):
        if os.path.exists(Settings.PATH):
            os.remove(Settings.PATH)

    def test_settings(self):
        expected_namespace = 'my_namespace'
        expected_redis = {'host': 'test.redis.io', 'port': '12345', 'password': 'secret-password'}
        self.assertEqual(expected_namespace, Settings.instance().namespace())
        self.assertEqual(expected_redis, Settings.instance().redis())

    def test_config_file(self):
        with open(self.TEMP_CONFIG_PATH, 'r') as f:
            expected = ("[main]\n"
                        "namespace = my_namespace\n\n"
                        "[redis]\n"
                        "host = test.redis.io\n"
                        "port = 12345\n"
                        "password = secret-password\n\n")
            self.assertEqual(expected, f.read())

    def __run_with_sample_prompt_value(self):
        prompt_input = ("my_namespace\n"
                        "test.redis.io\n"
                        "12345\n"
                        "secret-password\n")

        result = CliRunner().invoke(cli.configure, input=prompt_input)
        self.assertFalse(result.exception)
        self.assertEqual(0, result.exit_code)


class TestCliCopyPaste(unittest.TestCase):
    def setUp(self):
        RedisClipboard.instance().conn = fakeredis.FakeStrictRedis()

    def test_flow(self):
        runner = CliRunner()
        sample_data = os.urandom(1024)
        with runner.isolated_filesystem():
            with open('input.dat', 'wb') as input_file:
                input_file.write(sample_data)

            with open('input.dat', 'rb') as input_file:
                result = runner.invoke(cli.copy, 'input.dat')
                self.assertFalse(result.exception)
                self.assertEqual(0, result.exit_code)

            with open('output.dat', 'wb') as output_file:
                result = runner.invoke(cli.paste, 'output.dat')
                self.assertFalse(result.exception)
                self.assertEqual(0, result.exit_code)

            with open('output.dat', 'rb') as output_file:
                self.assertEqual(sample_data, output_file.read())
