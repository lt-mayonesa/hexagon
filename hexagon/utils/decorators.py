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


def for_all_methods(decorator, exclude=None):
    exclude = exclude or []

    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)) and attr not in exclude:
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate
