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
"""Autodoc extension for configurable traits.
This code auto documents traits from Cylc UI Server:
Acknowledgment:
    Code derived from the Jupyter Hub source (BSD).
    Copyright (c) 2015 Project Jupyter Contributors
    All rights reserved.
    https://github.com/jupyterhub/autodoc-traits/
        __init__.py
"""

__version__ = "0.1.0"


def setup(app, *args, **kwargs):
    from .autodoc_traits import setup

    return setup(app, *args, **kwargs)
