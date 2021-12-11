# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from pydash import py_
from importlib import import_module


def load_module_function(module_function_path: str):
    """Load function from a string.

    Args:
        module_function_path (str): Path to the function that will be loaded (In the format <module>:<function>).
    Returns:
        Callable: Loaded function.
    """
    module_path, module_fnc_name = module_function_path.split(":")

    mod = import_module(module_path)
    return getattr(mod, module_fnc_name)


def transform_object(obj, transformer_config):
    """Transform object properties based on a transformer configuration."""
    for key in transformer_config.keys():
        key_obj = transformer_config[key]
        key_fnc_args = {}

        key_fnc = key_obj
        if isinstance(key_obj, dict):
            key_fnc = key_obj["fnc"]
            key_fnc_args = key_obj["args"]

        key_transform_fnc = load_module_function(key_fnc)
        py_.set_(obj, key, key_transform_fnc(py_.get(obj, key), **key_fnc_args))

    return obj
