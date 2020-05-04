import app.version


class TestVersion():
    def test_version(self):
        assert '0.1.1' == app.version.VERSION
