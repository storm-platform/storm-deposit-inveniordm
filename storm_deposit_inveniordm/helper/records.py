# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from functools import wraps

from storm_deposit.deposit.models.api import DepositTask
from storm_project.project.records.api import ResearchProject


def pass_records(f):
    """Decorator to prepare a InvenioRDM client based on access token."""

    @wraps(f)
    def wrapper(deposit_id, invenio_client, *args, **kwargs):
        try:
            # loading the defined deposit record
            deposit_object = DepositTask.get_record(id=deposit_id)
            project_object = ResearchProject.get_record(id_=deposit_object.project.id)

        except:
            raise RuntimeError("Is not possible to load the Deposit record.")

        return f(
            deposit=deposit_object,
            project=project_object,
            invenio_client=invenio_client,
            *args,
            **kwargs
        )

    return wrapper
