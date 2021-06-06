def fill_args(args, size):
    return (list(args) + [None] * size)[:size] if size > 0 else list(args)
