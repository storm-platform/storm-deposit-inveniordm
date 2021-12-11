# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from . import config
from .tasks import service_task


class PluginService:
    service = service_task

    metadata = {
        "id": config.PLUGIN_SERVICE_NAME,
        "metadata": {
            "title": "InvenioRDM deposit plugin",
            "description": "Deposit plugin to send Storm WS workflows to Invenio RDM instances.",
        },
    }


def init_contrib(registry):
    """Initialize the InvenioRDM contrib services."""
    registry.register("deposit-inveniordm", PluginService)
