# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

PLUGIN_SERVICE_NAME = "deposit-inveniordm"

TEMPLATE_PATH = "inveniordm/template"

TRANSFORMER_CONFIG = {
    "metadata.subjects": {
        "fnc": "storm_deposit_inveniordm.transformer.operator:transform_list_to_dict",
        "args": {"key_field": "subject"},
    },
    "metadata.rights": {
        "fnc": "storm_deposit_inveniordm.transformer.operator:transform_list_with_lng_default_key",
        "args": {"field": "title", "language": "en"},
    },
    "metadata.dates": {
        "fnc": "storm_deposit_inveniordm.transformer.operator:transform_list_with_lng_default_key",
        "args": {"field": "type.id", "language": "en", "target": "type.title"},
    },
}
