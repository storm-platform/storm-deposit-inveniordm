# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from importlib import import_module
from storm_deposit_inveniordm.contrib import CONTRIB_MODULES


def init_plugins():
    """Initialize the plugin services in the flask app instance."""

    plugin_services = {}
    for module in CONTRIB_MODULES:
        mod = import_module(module)
        mod.init_contrib(plugin_services)

    return plugin_services


__all__ = "init_plugins"
