import time


def main(*_):
    time.sleep(1)
    raise Exception("This is an error")
