import io
import unittest

import fakeredis

from klippy.clipboard import RedisClipboard
from klippy.config import Settings


class TestRedisClipboard(unittest.TestCase):
    def setUp(self):
        self.original_settings_path = Settings.PATH
        Settings.PATH = "tests/.tmp.ini"
        self.subject = RedisClipboard(Settings())
        self.subject.conn = fakeredis.FakeStrictRedis()

    def tearDown(self):
        self.subject.conn.close()
        Settings.PATH = self.original_settings_path

    def test_copy(self):
        stream = io.BytesIO(b"test.copy")
        self.subject.copy(stream)
        self.assertEqual(b"test.copy", self.subject.conn.get(self.subject.store_key()))

    def test_paste(self):
        self.subject.conn.set(self.subject.store_key(), b"test.paste")
        stream = io.BytesIO()
        self.subject.paste(stream)
        stream.seek(0)
        self.assertEqual(b"test.paste", stream.read())

    def test_paste_empty(self):
        stream = io.BytesIO()
        self.subject.paste(stream)
        stream.seek(0)
        self.assertEqual(b"", stream.read())

    def test_copy_paste(self):
        in_stream = io.BytesIO(b"some.url.dot.com")
        out_stream = io.BytesIO()
        self.subject.copy(in_stream)
        self.subject.paste(out_stream)
        out_stream.seek(0)
        self.assertEqual(b"some.url.dot.com", out_stream.read())
