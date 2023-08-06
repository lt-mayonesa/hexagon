def silent_fail():
    """
    Decorator to call a function and catch any exception that might be raised.

    :return: a wrapper for the decorated function
    """

    def decorator(func):
        def wrapper():
            # noinspection PyBroadException
            try:
                return func()
            except Exception:
                return

        return wrapper

    return decorator
