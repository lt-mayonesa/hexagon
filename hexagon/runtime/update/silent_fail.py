def silent_fail(func):
    """
    Decorator to call a function and catch any exception that might be raised.

    :return: a wrapper for the decorated function
    """

    def wrapper():
        # noinspection PyBroadException
        try:
            return func()
        except Exception:
            return

    return wrapper
