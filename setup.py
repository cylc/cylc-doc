#!/usr/bin/env python
# coding=utf-8

# THIS FILE IS PART OF THE CYLC SUITE ENGINE.
# Copyright (C) 2008-2020 NIWA & British Crown (Met Office) & Contributors.
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
    'sphinx>=2.0.0,<3.0.0',
    'sphinx_rtd_theme>=0.5.0',
    'sphinxcontrib-svg2pdfconverter',
    'hieroglyph',
    'eralchemy==1.2.*',
    'cylc-sphinx-extensions'
]

EXTRAS_REQUIRE = {
    'test': [
        'pycodestyle'
    ],
    'tutorial': [
        'pillow'
    ]

}
EXTRAS_REQUIRE['all'] = [y for x in EXTRAS_REQUIRE.values() for y in x]


setup(
    name='cylc-doc',
    version=VERSION,
    long_description=open('README.md').read(),
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
