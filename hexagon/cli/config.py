import os

from ruamel.yaml import YAML


class Configuration:

    def __init__(self, path: str = None):
        self.project_path = path
        self.__config = None

    def init_config(self, path):
        self.project_path = os.environ['HEXAGON_CONFIG_FILE'].replace('app.yaml', '').replace('app.yml', '')
        __defaults = {
            'cli': {'name': 'Hexagon'},
            'tools': {
                'save-alias': {
                    'long_name': 'Save Last Command as Linux Alias',
                    'type': 'hexagon',
                    'action': 'hexagon.tools.internal.save_new_alias'
                },
                'create-tool': {
                    'long_name': 'Create A New Tool',
                    'type': 'hexagon',
                    'action': 'hexagon.tools.internal.create_new_tool'
                }
            },
            'envs': {}
        }
        try:
            with open(path, 'r') as f:
                self.__config = YAML().load(f)
        except FileNotFoundError:
            return self.__initial_setup_config()

        return (
            {
                **__defaults["cli"],
                **self.__config["cli"]
            },
            {**self.__add_hexagon_tools(__defaults)},
            {
                **__defaults["envs"],
                **self.__config['envs']
            }
        )

    def __add_hexagon_tools(self, __defaults):
        tools = self.__config['tools']
        tools.update(__defaults['tools'])
        return tools

    @staticmethod
    def __initial_setup_config():
        return (
            {'name': 'Hexagon'},
            {
                'install': {
                    'long_name': 'Install CLI',
                    'description': 'Install a custom project CLI from a YAML file.',
                    'type': 'hexagon',
                    'action': 'install_cli'
                }
            },
            {}
        )


configuration = Configuration()
cli, tools, envs = configuration.init_config(os.getenv('HEXAGON_CONFIG_FILE', 'app.yaml'))
