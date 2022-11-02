import os

import yaml


class YamlConfig:
    @staticmethod
    def read(yaml_file_name=None):
        if yaml_file_name is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            yaml_file_name = os.path.join(current_dir, 'config', 'config.yml')
        with open(yaml_file_name, 'r') as file:
            config = yaml.safe_load(file)
            return config
