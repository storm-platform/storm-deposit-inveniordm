# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

import storm_deposit_inveniordm.contrib.gkhub.config as config

from storm_deposit_inveniordm.contrib.gkhub.tasks import service_task
from storm_deposit_inveniordm.contrib.gkhub.proxies import gkhub_server_url


class PluginService:

    #
    # General definitions
    #
    id = config.PLUGIN_SERVICE_NAME

    #
    # Service task
    #
    service = service_task

    #
    # Editable Schema Fields
    #
    schema = None

    #
    # General plugin service description
    #
    metadata = {
        "title": "InvenioRDM deposit plugin",
        "description": "Deposit plugin to send Storm WS workflows to GEO Knowledge Hub instances.",
    }

    #
    # Extra fields availables
    #
    extras = {"url": gkhub_server_url}


def init_contrib(service_register):
    """Initialize the GEO Knowledge Hub contrib services."""
    service_register[PluginService.id] = PluginService
