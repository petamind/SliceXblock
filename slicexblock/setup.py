"""Setup for slicexblock XBlock."""

import os

from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='slicexblock-xblock',
    version='0.1',
    description='slicexblock XBlock',   # TODO: write a better description.
    license='GPL v3',          # TODO: choose a license: 'AGPL v3' and 'Apache 2.0' are popular.
    packages=[
        'slicexblock',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'slicexblock = slicexblock:SliceXBlock',
        ]
    },
    package_data=package_data("slicexblock", ["static", "public"]),
)
