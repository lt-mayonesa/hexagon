import os

from halo import Halo


def with_spinner(text):
    """
    Decorator to display a spinner for long running processes.

    :param text: the text to be displayed beside the spinner
    :return: a wrapper for the decorated function
    """
    spinner_disabled = bool(os.getenv("HEXAGON_DISABLE_SPINNER", ""))

    def decorator(func):
        def wrapper(*args, **kwargs):
            if spinner_disabled:
                return func(*args, **kwargs)
            else:
                with Halo(text=text):
                    return func(*args, **kwargs)

        return wrapper

    return decorator
