import os

from ruamel.yaml import YAML

CONFIG_FILE_ENV_VARIABLE_NAME = 'HEXAGON_CONFIG_FILE'


class Configuration:

    def __init__(self, path: str = None):
        self.project_path = path
        self.project_yaml = None
        self.__config = None

    def init_config(self, path):
        if CONFIG_FILE_ENV_VARIABLE_NAME in os.environ:
            self.project_yaml = os.environ[CONFIG_FILE_ENV_VARIABLE_NAME]
            self.project_path = self.project_yaml.replace('app.yaml', '').replace('app.yml', '')

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
                **__defaults['cli'],
                **self.__config['cli']
            },
            {
                **self.__config['tools'],
                **__defaults['tools']
            },
            {
                **__defaults['envs'],
                **self.__config['envs']
            }
        )

    def refresh(self):
        return self.init_config(self.project_yaml)

    def save(self):
        with open(self.project_yaml, 'w') as f:
            YAML().dump(self.__config, f)
        return self.__config['cli'], self.__config['tools'], self.__config['envs']

    def add_tool(self, command, config):
        self.__config['tools'].insert(len(self.__config['tools']), command, config)
        self.__config['tools'].yaml_set_comment_before_after_key(command, before='\n')

    def set(self, key, value, comment=None, position=0):
        self.__config['cli'].insert(position, key, value, comment)

    @staticmethod
    def __initial_setup_config():
        return (
            {'name': 'Hexagon'},
            {
                'install': {
                    'long_name': 'Install CLI',
                    'description': 'Install a custom project CLI from a YAML file.',
                    'type': 'hexagon',
                    'action': 'hexagon.tools.internal.install_cli'
                }
            },
            {}
        )


configuration = Configuration()
cli, tools, envs = configuration.init_config(os.getenv('HEXAGON_CONFIG_FILE', 'app.yaml'))
