import unittest

import io
import fakeredis

from app.clipboard import RedisClipboard


class TestRediClipboard(unittest.TestCase):
    def setUp(self):
        self.subject = RedisClipboard().instance()
        self.subject.conn = fakeredis.FakeStrictRedis()

    def tearDown(self):
        self.subject.conn.close()

    def test_copy(self):
        stream = io.BytesIO(b'test.copy')
        self.subject.copy(stream)
        self.assertEqual(b'test.copy', self.subject.conn.get(self.subject.STORE_KEY))

    def test_paste(self):
        self.subject.conn.set(self.subject.STORE_KEY, b'test.paste')
        stream = io.BytesIO()
        self.subject.paste(stream)
        stream.seek(0)
        self.assertEqual(b'test.paste', stream.read())

    def test_copy_paste(self):
        in_stream = io.BytesIO(b'some.url.dot.com')
        out_stream = io.BytesIO()
        self.subject.copy(in_stream)
        self.subject.paste(out_stream)
        out_stream.seek(0)
        self.assertEqual(b'some.url.dot.com', out_stream.read())
