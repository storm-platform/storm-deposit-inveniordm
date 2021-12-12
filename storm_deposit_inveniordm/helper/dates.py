# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from datetime import datetime


def date_now_iso8601():
    """Generate a complete ISO8601 date string with the actual date."""
    return datetime.today().strftime("%Y-%m-%d")
