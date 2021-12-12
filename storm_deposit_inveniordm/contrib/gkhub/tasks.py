# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

import shutil
import tempfile
from pathlib import Path

import bagit
from pydash import py_

from celery import shared_task

from storm_client_invenio.models.record import RecordDraft
from storm_pipeline.pipeline.records.api import ResearchPipeline
from storm_compendium.compendium.records.api import CompendiumRecord

import storm_deposit_inveniordm.contrib.gkhub.config as config

from storm_deposit_inveniordm.contrib.gkhub.proxies import (
    gkhub_datacite_id,
    gkhub_server_url,
)

from storm_deposit_inveniordm.helper.dates import date_now_iso8601
from storm_deposit_inveniordm.helper.template import render_template
from storm_deposit_inveniordm.transformer.transformer import transform_object

from storm_deposit_inveniordm.helper.records import pass_records
from storm_deposit_inveniordm.helper.invenio import pass_invenio_client


@shared_task
@pass_invenio_client(gkhub_server_url)
@pass_records
def service_task(deposit, project, invenio_client, **kwargs):
    """Service task to prepare and send the project to an InvenioRDM instance."""

    # Preparing the Knowledge Package metadata
    knowledge_package = transform_object(project, config.TRANSFORMER_CONFIG)
    knowledge_package = render_template(
        "knowledge-package.json",
        config.TEMPLATE_PATH,
        kpackage=knowledge_package,
        now=date_now_iso8601(),
    )

    knowledge_package = RecordDraft(knowledge_package)
    knowledge_package = invenio_client.records.draft().create(knowledge_package)

    # Preparing the Knowledge Resources files and metadata
    knowledge_package_parts = []
    tempdir = Path(tempfile.mkdtemp())

    for pipeline in deposit.pipelines:
        pipeline = ResearchPipeline.get_record(id_=pipeline.id)

        pipeline_vertices = list(pipeline.graph["nodes"].keys())
        pipeline_vertices = py_.map(pipeline_vertices, CompendiumRecord.pid.resolve)

        # Preparing the package
        package_dir = tempdir / pipeline.pid.pid_value
        package_dir_data = package_dir / "data"

        for pipeline_vertex in pipeline_vertices:

            pipeline_vertex_id = pipeline_vertex.pid.pid_value

            pipeline_vertex_data = package_dir_data / pipeline_vertex_id
            pipeline_vertex_data.mkdir(parents=True)

            files_entries = pipeline_vertex.files.entries
            for pipeline_vertex_file in files_entries:
                file_entry = files_entries[pipeline_vertex_file]
                file_source = Path(file_entry.file.file_model.uri)
                file_target = pipeline_vertex_data / pipeline_vertex_file

                shutil.copy(file_source, file_target)

        # Creating the bagit file
        zip_file = tempdir / pipeline.pid.pid_value

        bagit.make_bag(package_dir_data)
        shutil.make_archive(zip_file, "zip", package_dir_data)

        # Uploading the pipeline record
        knowledge_resource = render_template(
            "knowledge-resource.json",
            config.TEMPLATE_PATH,
            project=project,
            kpackage=knowledge_package,
            pipeline=pipeline,
            instance_pid=gkhub_datacite_id,
            now=date_now_iso8601(),
        )

        knowledge_resource = RecordDraft(knowledge_resource)
        knowledge_resource = invenio_client.records.draft().create(knowledge_resource)

        zip_file = f"{zip_file}.zip"
        invenio_client.records.files(knowledge_resource).upload_files(
            {Path(zip_file).name: zip_file},
            commit=True,
        )

        # Saving the knowledge resource reference.
        knowledge_package_parts.append(
            {
                "identifier": f"{gkhub_datacite_id}/{knowledge_resource.id}",
                "scheme": "doi",
                "relation_type": {"id": "haspart", "title": {"en": "Has part"}},
            }
        )

        # Excluding the data directory file
        shutil.rmtree(package_dir)

    # Linking the knowledge resources with the Knowledge Package
    knowledge_package["metadata"]["related_identifiers"] = knowledge_package_parts

    invenio_client.records.draft().save(knowledge_package)
