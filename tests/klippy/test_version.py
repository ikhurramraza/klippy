import klippy.version


class TestVersion:
    def test_version(self):
        assert "0.2.0" == klippy.version.VERSION
