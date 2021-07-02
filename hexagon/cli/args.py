def fill_args(args, size):
    return (list(args) + [None] * size)[:size] if size > 0 else list(args)


def cli_arg(cli_args, index):
    return cli_args[index] if cli_args and len(cli_args) > index else None
