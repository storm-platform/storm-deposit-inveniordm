# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit-inveniordm is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Plugin to enable deposit operations in InvenioRDM instances."""

import os

from setuptools import find_packages, setup

readme = open("README.rst").read()
history = open("CHANGES.rst").read()

tests_require = []

extras_require = {
    "docs": [
        "Sphinx>=3,<4",
    ],
    "tests": tests_require,
}

extras_require["all"] = [req for _, reqs in extras_require.items() for req in reqs]

setup_requires = []

install_requires = [
    "pydash>=5.1.0,<6.0",
    "bagit>=1.8.1,<2",
    # Storm dependencies
    "storm-project @ git+https://github.com/storm-platform/storm-project",
    "storm-pipeline @ git+https://github.com/storm-platform/storm-pipeline",
    "storm-commons @ git+https://github.com/storm-platform/storm-compendium",
    "storm-client-invenio @ git+https://github.com/storm-platform/storm-client-invenio",
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join("storm_deposit_inveniordm", "version.py"), "rt") as fp:
    exec(fp.read(), g)
    version = g["__version__"]

setup(
    name="storm-deposit-inveniordm",
    version=version,
    description=__doc__,
    long_description=readme + "\n\n" + history,
    keywords="invenio TODO",
    license="MIT",
    author="Felipe Menino Carlos",
    author_email="felipe.carlos@inpe.br",
    url="https://github.com/storm-platform/storm-deposit-inveniordm",
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    entry_points={
        "storm_deposit.plugins": [
            "storm-deposit-inveniordm = storm_deposit_inveniordm:StormDepositInvenioRDM"
        ],
        "invenio_celery.tasks": [
            "storm_deposit_gkhub = storm_deposit_inveniordm.contrib.gkhub.tasks",
            "storm_deposit_inveniordm = storm_deposit_inveniordm.contrib.inveniordm.tasks",
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 1 - Planning",
    ],
)
