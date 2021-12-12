# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

import storm_deposit_inveniordm.config as config
from storm_deposit_inveniordm.contrib.plugin import init_plugins


class StormDepositInvenioRDM:
    """Flask extension for the Storm Deposit InvenioRDM service plugin."""

    def __init__(self, app=None):
        """Plugin initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.init_plugin_services(app)

        app.extensions["storm-deposit-inveniordm"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("STORM_DEPOSIT_"):
                app.config.setdefault(k, getattr(config, k))

    def init_plugin_services(self, app):
        """Initialize the plugin services."""
        self.plugin_services = init_plugins()


__all__ = "StormDepositInvenioRDM"
