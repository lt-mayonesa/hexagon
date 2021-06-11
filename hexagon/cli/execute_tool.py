import sys

from rich import print


def __load_module(module):
    # module_path = "mypackage.%s" % module
    module_path = module

    if module_path in sys.modules:
        return sys.modules[module_path]

    return __import__(module_path, fromlist=[module])


def register_external_tools(src: dict):
    if 'custom_tools_dir' in src:
        sys.path.append(src['custom_tools_dir'])


def execute_action(action: str, args):
    try:
        tool = __load_module(action)
    except ModuleNotFoundError:
        tool = __load_module(f'hexagon.tools.{action}')

    try:
        tool.main(args)
    except AttributeError:
        print(f'[red]Tool {action} does not have the required `main(args...)` function.')
        sys.exit(1)
