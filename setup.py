#!/usr/bin/env python3

from setuptools import setup
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('linkbot_internal_dev/linkbot_internal_dev.py').read(),
    re.M
    ).group(1)

setup(
    name = "linkbot_internal_dev",
    packages = ["linkbot_internal_dev", "linkbot_internal_dev.forms"],
    version = version,
    entry_points = {
        "console_scripts":
        [
         'linkbot-internal-dev=linkbot_internal_dev.linkbot_internal_dev:main',
        ]
    },
    install_requires = ["PyLinkbot3 >= 3.1.2", "linkbot_diagnostics >= 0.2.2"],
    description = "Tool for testing Linkbots",
    zip_safe = False,
    include_package_data = True,
    author = "David Ko",
    author_email = "david@barobo.com",
    )

