import pytest

from hexagon.cli.args import fill_args


def test_empty_args():
    assert fill_args([], 0) == []
    assert fill_args([], 1) == [None]
    assert fill_args([], 3) == [None, None, None]
    assert fill_args([], 9) == [None, None, None, None, None, None, None, None, None]


@pytest.mark.parametrize(
    "args,fill,expected",
    [
        (["/path"], 0, ["/path"]),
        (["/path"], 1, ["/path"]),
        (["/path", "1"], 3, ["/path", "1", None]),
        (["/path"], 9, ["/path", None, None, None, None, None, None, None, None]),
    ],
)
def test_some_args(args, fill, expected):
    assert fill_args(args, fill) == expected
