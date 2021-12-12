# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

import marshmallow as ma

from marshmallow_utils.fields import SanitizedUnicode
from storm_commons.schema.validators import marshmallow_not_blank_field


class InvenioRDMExtSchema(ma.Schema):
    """InvenioRDM metadata customizable fields schema."""

    title = SanitizedUnicode(
        required=True, validate=marshmallow_not_blank_field(max=250)
    )
    description = SanitizedUnicode(validate=marshmallow_not_blank_field(max=2000))
