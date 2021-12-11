# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from pydash import py_
from typing import List

from invenio_client import InvenioRDM

from storm_project.project.records.api import ResearchProject
from storm_pipeline.pipeline.records.api import ResearchPipeline

from .contrib.registry import ContribRegistry

from . import config


class StormDepositInvenioRDM:

    plugin_services = ContribRegistry.list_services_metadata()

    @staticmethod
    def entrypoint(
        service_name: str, project_id: str, pipeline_ids: List[str], **kwargs
    ):
        # Selecting the records
        selected_project = ResearchProject.pid.resolve(project_id)
        selected_pipelines = py_.map(pipeline_ids, ResearchPipeline.pid.resolve)

        # Defining the contrib service
        selected_deposit_service = ContribRegistry.service(service_name)

        # Creating invenio client instance
        invenio_service_url = selected_deposit_service.extras.get("url")
        invenio_service_token = kwargs.get("access_token")

        if not invenio_service_token:
            raise RuntimeError("Access token not defined!")

        invenio_service_client = InvenioRDM(
            invenio_service_url._get_current_object(), invenio_service_token
        )
        selected_deposit_service.service(
            project=selected_project,
            pipelines=selected_pipelines,
            invenio_client=invenio_service_client,
        )

    def __init__(self, app=None):
        """Plugin initialization."""
        if app:
            self.init_plugin(app)

    def init_plugin(self, app):
        """Flask application initialization."""
        self.init_config(app)

        app.extensions["storm-deposit-inveniordm"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("STORM_DEPOSIT_"):
                app.config.setdefault(k, getattr(config, k))


__all__ = "StormDepositInvenioRDM"
