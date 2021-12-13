# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from functools import wraps
from storm_client_invenio import InvenioRDM

from werkzeug.local import LocalProxy


def pass_invenio_client(url_server_proxy: LocalProxy):
    """Wrapper decorator function to define a specific service url
    to use in the InvenioRDM client factory.

    Args:
        url_server_proxy (LocalProxy): Proxy to service url used in the InvenioRDM client instance.

    Returns:
        Callable: Wrapper invenio client decorator.
    """

    def invenio_client_decorator(f):
        """Decorator to prepare a InvenioRDM client based on access token."""

        @wraps(f)
        def wrapper(deposit_id, data, *args, **kwargs):
            try:
                access_token = data.get("access_token")

                if not access_token:
                    raise RuntimeError("Invalid `access_token`")

                invenio_client = InvenioRDM(
                    url_server_proxy._get_current_object(), access_token
                )
            except:
                raise RuntimeError(
                    "Is not possible to create the InvenioRDM client instance."
                )

            return f(
                deposit_id=deposit_id, invenio_client=invenio_client, *args, **kwargs
            )

        return wrapper

    return invenio_client_decorator
