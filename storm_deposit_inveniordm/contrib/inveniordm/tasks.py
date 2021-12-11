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
from typing import List

from pathlib import Path

from celery import shared_task

from storm_client_invenio import InvenioRDM
from storm_client_invenio.models.record import RecordDraft

from storm_project.project.records.api import ResearchProject
from storm_pipeline.pipeline.records.api import ResearchPipeline
from storm_compendium.compendium.records.api import CompendiumRecord

from . import config
from ...template import render_template
from ...transformer.transformer import transform_object
from ...utils import date_now_iso8601


@shared_task
def service_task(
    project: ResearchProject,
    pipelines: List[ResearchPipeline],
    invenio_client: InvenioRDM = None,
    **kwargs,
):
    """Service task to prepare and send the project to an InvenioRDM instance."""

    # Preparing the metadata
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

    for pipeline in pipelines:
        pipeline_vertices = list(pipeline.graph["nodes"].keys())
        pipeline_vertices = py_.map(pipeline_vertices, CompendiumRecord.pid.resolve)

        """
        Zip hierarchy:
         - pipeline
          - <pipeline-id>
            - <file>
            - <file>
            ...
          - <pipeline-id>
            - <file>
            - <file>
            - ...
          ...
        """

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

        # saving the zip file
        zip_files.append(f"{zip_file}.zip")

        shutil.rmtree(package_dir)

    created_draft = RecordDraft(project_metadata)
    created_draft = invenio_client.records.draft().create(created_draft)

    invenio_client.records.files(created_draft).upload_files(
        {Path(file).name: file for file in zip_files},
        commit=True,
    )
