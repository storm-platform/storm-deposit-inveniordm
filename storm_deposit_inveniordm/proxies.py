# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from flask import current_app
from werkzeug.local import LocalProxy


current_storm_deposit_inveniordm = LocalProxy(
    lambda: current_app.extensions["storm-deposit-inveniordm"]
)
"""Helper proxy to get the current Storm Deposit InvenioRDM extension."""
