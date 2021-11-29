#!/usr/bin/env python
# coding=utf-8

# THIS FILE IS PART OF THE CYLC WORKFLOW ENGINE.
# Copyright (C) NIWA & British Crown (Met Office) & Contributors.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from setuptools import setup


HERE = Path(__file__).resolve().parent


def get_version(module, path):
    """Return the __version__ attr from a module sourced by FS path."""
    spec = spec_from_file_location(module, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__


VERSION = get_version(
    'cylc.doc',
    str(Path(HERE, 'cylc/doc/__init__.py'))
)

INSTALL_REQUIRES = [
    'cylc-sphinx-extensions>=1.3.3',
    'eralchemy==1.2.*',
    'hieroglyph>=2.1.0',
    'setuptools>=50',
    'sphinx>=3.0.0',
    'sphinx_rtd_theme>=0.5.0',
    'sphinxcontrib-svg2pdfconverter',
]

EXTRAS_REQUIRE = {
    'test': [
        'flake8',
        'flake8-broken-line>=0.3.0',
        'flake8-bugbear>=21.0.0',
        'flake8-builtins>=1.5.0',
        'flake8-comprehensions>=3.5.0',
        'flake8-debugger>=4.0.0',
        'flake8-mutable>=1.2.0',
        'flake8-simplify>=0.14.0',
    ],
    'tutorial': [
        'pillow',
        'urllib3'
    ]

}
EXTRAS_REQUIRE['all'] = [y for x in EXTRAS_REQUIRE.values() for y in x]


with open('README.md', 'r') as readmefile:
    README = readmefile.read()


setup(
    name='cylc-doc',
    version=VERSION,
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    project_urls={
        "Documentation": "https://cylc.github.io/documentation.html",
        "Source": "https://github.com/cylc/cylc-doc",
        "Tracker": "https://github.com/cylc/cylc-doc/issues"
    },
    package_data={
        'cylc.doc': ['etc/tutorial/']
    },
)
