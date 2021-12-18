# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

import storm_deposit_inveniordm.contrib.inveniordm.config as config
from storm_deposit_inveniordm.contrib.inveniordm.tasks import service_task
from storm_deposit_inveniordm.contrib.inveniordm.proxies import invenio_rdm_server_url

from storm_deposit_inveniordm.contrib.inveniordm.schema import InvenioRDMExtSchema


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
    schema = InvenioRDMExtSchema

    #
    # General plugin service description
    #
    metadata = {
        "title": "InvenioRDM deposit plugin",
        "description": "Deposit plugin to send Storm WS workflows to Invenio RDM instances.",
        "customizable-metadata-fields": ["title", "description"]
    }

    #
    # Extra fields availables
    #
    extras = {"url": invenio_rdm_server_url}


def init_contrib(service_register):
    """Initialize the InvenioRDM contrib services."""
    service_register[PluginService.id] = PluginService
