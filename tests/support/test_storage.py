import pytest

from hexagon.support.storage import _resolve_storage_path

BASE_DIR = "~/.hexagon"


@pytest.mark.parametrize(
    "app,key,expected",
    [
        ("hexagon", "file", (f"{BASE_DIR}/hexagon", "file")),
        (
            "foo",
            "test.nested.nested2.file",
            (f"{BASE_DIR}/foo/test/nested/nested2", "file"),
        ),
    ],
)
def test_resolve_storage_path(app, key, expected):
    assert _resolve_storage_path(app, key, BASE_DIR) == expected
