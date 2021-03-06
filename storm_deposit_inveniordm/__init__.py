# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Plugin to enable deposit operations in InvenioRDM instances."""

from .version import __version__
from .ext import StormDepositInvenioRDM

__all__ = ("StormDepositInvenioRDM", "__version__")
