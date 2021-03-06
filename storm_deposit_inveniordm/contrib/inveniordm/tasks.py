# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

import bagit
import shutil
import tempfile

from pydash import py_

from pathlib import Path

from celery import shared_task

from storm_client_invenio.models.record import RecordDraft
from storm_workflow.workflow.records.api import ResearchWorkflow
from storm_compendium.compendium.records.api import CompendiumRecord

import storm_deposit_inveniordm.contrib.inveniordm.config as config

from storm_deposit_inveniordm.helper.dates import date_now_iso8601
from storm_deposit_inveniordm.helper.template import render_template
from storm_deposit_inveniordm.transformer.transformer import transform_object

from storm_deposit_inveniordm.helper.records import pass_records
from storm_deposit_inveniordm.helper.invenio import pass_invenio_client
from storm_deposit_inveniordm.contrib.inveniordm.proxies import invenio_rdm_server_url


@shared_task
@pass_invenio_client(invenio_rdm_server_url)
@pass_records
def service_task(deposit, project, invenio_client, **kwargs):
    """Service task to prepare and send the project to an InvenioRDM instance."""

    # Checking for a custom fields definition.
    custom_fields_metadata = deposit.customizations or {}

    if custom_fields_metadata:
        project.metadata.update(custom_fields_metadata)

    # Preparing the record metadata.
    project_metadata = transform_object(project, config.TRANSFORMER_CONFIG)
    project_metadata = render_template(
        "metadata.json",
        config.TEMPLATE_PATH,
        project=project,
        now=date_now_iso8601(),
    )

    # Organizing the files
    zip_files = []
    tempdir = Path(tempfile.mkdtemp())

    for workflow in deposit.workflows:
        workflow = ResearchWorkflow.get_record(id_=workflow.id)

        workflow_vertices = list(workflow.graph["nodes"].keys())
        workflow_vertices = py_.map(workflow_vertices, CompendiumRecord.pid.resolve)

        # Preparing the package
        package_dir = tempdir / workflow.pid.pid_value
        package_dir_data = package_dir / "data"

        for workflow_vertex in workflow_vertices:

            workflow_vertex_id = workflow_vertex.pid.pid_value

            workflow_vertex_data = package_dir_data / workflow_vertex_id
            workflow_vertex_data.mkdir(parents=True)

            files_entries = workflow_vertex.files.entries
            for workflow_vertex_file in files_entries:
                file_entry = files_entries[workflow_vertex_file]
                file_source = Path(file_entry.file.file_model.uri)
                file_target = workflow_vertex_data / workflow_vertex_file

                shutil.copy(file_source, file_target)

        # Creating the bagit file
        zip_file = tempdir / workflow.pid.pid_value

        bagit.make_bag(package_dir_data)
        shutil.make_archive(zip_file, "zip", package_dir_data)

        # saving the zip file
        zip_files.append(f"{zip_file}.zip")

        shutil.rmtree(package_dir)

    created_draft = RecordDraft(project_metadata)
    created_draft = invenio_client.records.draft().create(created_draft)

    invenio_client.records.files(created_draft).upload_files(
        {Path(file).name: file for file in zip_files},
        commit=True,
    )
