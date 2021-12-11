# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from pydash import py_
from typing import Sequence


def transform_list_to_dict(obj, key_field=None, **kwargs):
    """Transform a list of elements in a list of objects identifier by an `id` key."""
    if not isinstance(obj, Sequence):
        raise ValueError("The `obj` argument must be a valid sequence type.")

    return py_.map(obj, lambda x: {key_field: x})


def transform_list_with_lng_default_key(
    obj, field=None, language=None, target=None, **kwargs
):
    """Add a key `en` into a given object property."""
    if not isinstance(obj, Sequence):
        raise ValueError("The `obj` argument must be a valid sequence type.")

    # auxiliary function
    def _transform(obj_to_transform, fld, lng, tgt):
        """Function to transform the objects."""

        field_path = f"{tgt}.{lng}"
        value_field = py_.get(obj_to_transform, fld)
        value_target = py_.get(obj_to_transform, tgt)

        if fld:
            if value_target != dict:
                py_.set_(obj_to_transform, tgt, {})
            py_.set_(obj_to_transform, field_path, value_field)

        return obj_to_transform

    default_field = field or ""
    default_target = target or default_field
    default_language = language or "en"
    return py_.map(
        obj,
        lambda x: _transform(x, default_field, default_language, default_target),
    )
