import os
import sys

import toml
from os import path


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def load_config_with_env(filepath: str):
    if path.exists(filepath):
        return toml.load(filepath, AttrDict)
    else:
        toml_config = os.environ.get('TOML_CONFIG')
        if toml_config is None:
            exit_with_message(f"The file {filepath} is not found")
            return
        return toml.loads(toml_config.encode('latin1').decode('unicode_escape'), AttrDict)


config = load_config_with_env('config.toml')


def exit_with_message(message: str):
    print(f"config: {message}")
    print(f"see 'config.example.toml' for more details on how to fill the required values in 'config.toml'")
    sys.exit(0)


example_config = toml.load('config.example.toml')

for config_section, example_config_section_dict in example_config.items():
    if config_section not in config:
        exit_with_message(f"missing section [{config_section}]")

    config_section_dict = config[config_section]
    for example_config_key, example_config_val in example_config_section_dict.items():
        if example_config_key not in config_section_dict:
            exit_with_message(f"missing key [{config_section}.{example_config_key}]")

        config_val = config_section_dict[example_config_key]
        if type(config_val) is not type(example_config_val):
            exit_with_message(
                f"type of field [{config_section}.{example_config_key}] should be of type '{type(example_config_val).__name__}'")
