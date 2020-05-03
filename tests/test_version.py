import unittest

import app.version


class TestVersion(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_version(self):
        self.assertEqual('0.1.1', app.version.VERSION)


if __name__ == '__main__':
    unittest.main()
