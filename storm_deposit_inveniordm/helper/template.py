# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

import ast
from storm_commons.template import render_template as render_template_base


def render_template(template_name: str, package_path: str, **template_objects):
    """Render a `storm-deposit-inveniordm` contrib template."""

    # rendering!
    rendered_template = render_template_base(
        template_name,
        "storm_deposit_inveniordm.contrib",
        package_path,
        **template_objects
    )

    rendered_template = rendered_template.replace("\n", "").replace("'", '"')
    return ast.literal_eval(rendered_template)


__all__ = "render_template"
