#!/usr/bin/env python3

import os
import ujson


def file_exists(path):
    try:
        os.stat(path)
        return True
    except OSError:
        return False


def load_config(config_file: str):
    """Load a JSON configuration file


    Parameters
    ----------
    conig_file : str
        The path to the configuration file.
    """
    with open(config_file) as f:
        return ujson.load(f)
