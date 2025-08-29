#!/usr/bin/env python3

import os
import ujson


def file_exists(path: str) -> bool:
    """Check if a given file exists.


    Parameters
    ----------
    path : str
        The path to the file.
    """
    try:
        os.stat(path)
        return True
    except OSError:
        return False


def load_config(config_file: str) -> Any:
    """Load a JSON configuration file.


    Parameters
    ----------
    config_file : str
        The path to the configuration file.
    """
    with open(config_file) as f:
        return ujson.load(f)


def validate_config(config: Any, schema: Dict) -> Any:
    """Validate the config read from a JSON file.

    This checks for required parameters and the desired parameter type.

    Parameters
    ----------
    config : Dict
        The config read from the config file.
    schema : Dict
        The required configuration schema.
    """
    errors = []

    for key, expected_type in schema.items():
        value = config.get(key)
        if value is None:
            errors.append(f"Missing required config key: '{key}'")
        elif not isinstance(value, expected_type):
            errors.append(
                f"Config key '{key}' must be of type {expected_type.__name__}, got {type(value).__name__}"
            )

    if errors:
        raise ValueError("\n".join(errors))
