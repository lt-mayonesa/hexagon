import sys


def fill_args(size):
    return (list(sys.argv) + [None] * size)[:size]
