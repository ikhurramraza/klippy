import os
import unittest
from unittest import mock

import fakeredis
from click.testing import CliRunner

from klippy import cli
from klippy.config import Settings


class CliTestCase(unittest.TestCase):
    TEMP_CONFIG_PATH = "tests/.tmp.ini"

    def setUp(self):
        self.original_settings_path = Settings.PATH
        Settings.PATH = self.TEMP_CONFIG_PATH

        self.server = fakeredis.FakeServer()
        patcher = mock.patch(
            "klippy.clipboard.redis.Redis",
            lambda **kwargs: fakeredis.FakeStrictRedis(server=self.server),
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self):
        if os.path.exists(Settings.PATH):
            os.remove(Settings.PATH)
        Settings.PATH = self.original_settings_path


class TestCliConfigure(CliTestCase):
    def setUp(self):
        super().setUp()
        self.__run_with_sample_prompt_value()

    def test_settings(self):
        expected_namespace = "my_namespace"
        expected_redis = {
            "host": "test.redis.io",
            "port": "12345",
            "password": "secret-password",
        }
        self.assertEqual(expected_namespace, Settings().namespace())
        self.assertEqual(expected_redis, Settings().redis())

    def test_config_file(self):
        with open(self.TEMP_CONFIG_PATH, "r") as f:
            expected = (
                "[main]\n"
                "namespace = my_namespace\n\n"
                "[redis]\n"
                "host = test.redis.io\n"
                "port = 12345\n"
                "password = secret-password\n\n"
            )
            self.assertEqual(expected, f.read())

    def test_password_is_not_echoed(self):
        self.assertNotIn("secret-password", self.configure_result.output)

    def test_reconfigure_preserves_password(self):
        result = CliRunner().invoke(cli.configure, input="\n\n\n\n")
        self.assertFalse(result.exception)
        self.assertEqual(0, result.exit_code)
        self.assertEqual("secret-password", Settings().redis()["password"])
        self.assertNotIn("secret-password", result.output)

    def __run_with_sample_prompt_value(self):
        prompt_input = "my_namespace\n" "test.redis.io\n" "12345\n" "secret-password\n"

        self.configure_result = CliRunner().invoke(cli.configure, input=prompt_input)
        self.assertFalse(self.configure_result.exception)
        self.assertEqual(0, self.configure_result.exit_code)


class TestCliDoctor(CliTestCase):
    def test_success(self):
        result = CliRunner().invoke(cli.doctor)
        self.assertFalse(result.exception)
        self.assertEqual(0, result.exit_code)
        self.assertIn(f"Settings file: {Settings.PATH}", result.output)
        self.assertIn("Namespace: default", result.output)
        self.assertIn("Connection: OK", result.output)

    def test_connection_failure(self):
        self.server.connected = False
        result = CliRunner().invoke(cli.doctor)
        self.assertEqual(1, result.exit_code)
        self.assertIn("Connection failed.", result.output)


class TestCliCopyPaste(CliTestCase):
    def test_copy_with_expire(self):
        result = CliRunner().invoke(cli.copy, ["--expire", "5m"], input=b"sample")
        self.assertEqual(0, result.exit_code)
        conn = fakeredis.FakeStrictRedis(server=self.server)
        self.assertAlmostEqual(300, conn.ttl("klippy.default"), delta=30)

    def test_copy_with_expire_in_seconds(self):
        result = CliRunner().invoke(cli.copy, ["-e", "90s"], input=b"sample")
        self.assertEqual(0, result.exit_code)
        conn = fakeredis.FakeStrictRedis(server=self.server)
        self.assertAlmostEqual(90, conn.ttl("klippy.default"), delta=30)

    def test_copy_with_invalid_expire(self):
        for invalid in ["abc", "90", "5x", "0s"]:
            result = CliRunner().invoke(cli.copy, ["--expire", invalid], input=b"sample")
            self.assertEqual(2, result.exit_code)

    def test_copy_connection_failure(self):
        self.server.connected = False
        result = CliRunner().invoke(cli.copy, input=b"sample")
        self.assertEqual(1, result.exit_code)
        self.assertIn("Copy failed", result.output)

    def test_paste_connection_failure(self):
        self.server.connected = False
        result = CliRunner().invoke(cli.paste)
        self.assertEqual(1, result.exit_code)
        self.assertIn("Paste failed", result.output)

    def test_flow(self):
        runner = CliRunner()
        sample_data = os.urandom(1024)
        with runner.isolated_filesystem():
            with open("input.dat", "wb") as input_file:
                input_file.write(sample_data)

            result = runner.invoke(cli.copy, "input.dat")
            self.assertFalse(result.exception)
            self.assertEqual(0, result.exit_code)

            result = runner.invoke(cli.paste, "output.dat")
            self.assertFalse(result.exception)
            self.assertEqual(0, result.exit_code)

            with open("output.dat", "rb") as output_file:
                self.assertEqual(sample_data, output_file.read())


class TestCliClear(CliTestCase):
    def test_clear(self):
        runner = CliRunner()
        result = runner.invoke(cli.copy, input=b"sample")
        self.assertEqual(0, result.exit_code)

        result = runner.invoke(cli.clear)
        self.assertEqual(0, result.exit_code)
        self.assertIn("Clipboard cleared.", result.output)

        conn = fakeredis.FakeStrictRedis(server=self.server)
        self.assertIsNone(conn.get("klippy.default"))

    def test_clear_connection_failure(self):
        self.server.connected = False
        result = CliRunner().invoke(cli.clear)
        self.assertEqual(1, result.exit_code)
        self.assertIn("Clear failed", result.output)
