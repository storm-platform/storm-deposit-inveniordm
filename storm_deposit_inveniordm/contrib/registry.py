# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from pydash import py_
from importlib import import_module

from . import CONTRIB_MODULES


class ContribRegistry:
    _contrib_modules = {}

    @classmethod
    def register(cls, name, service):
        """Register a new plugin service."""
        cls._contrib_modules[name] = service

    @classmethod
    def exists(cls, name):
        """Check if a plugin service exists."""
        return name in cls._contrib_modules

    @classmethod
    def service(cls, name):
        """Retrieve an existing plugin."""
        if cls.exists(name):
            return cls._contrib_modules[name]
        raise NotImplemented("Selected contrib module not found.")

    @classmethod
    def list_services_metadata(cls):
        """List the available services metadata."""
        return py_.map(cls._contrib_modules.values(), lambda x: x.metadata)

    @classmethod
    def initialize(cls, modules):
        """Initialize the registry with N services."""
        for module in modules:
            mod = import_module(module)
            mod.init_contrib(cls)


ContribRegistry.initialize(CONTRIB_MODULES)


__all__ = "ContribRegistry"
