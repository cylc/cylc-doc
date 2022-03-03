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

"""Easily document enum values for user facing interfaces.

Useful for cases where the enum itself is not a user-facing interface but
describes values which are user-facing.

Results in the following format:

<enum docstring />
<enum.Value1.value />
    <enum.Value1.docstring />
<enum.Value2.value />
    <enum.Value2.docstring />

"""

from inspect import cleandoc, getsource
from importlib import import_module

from docutils.parsers.rst import Directive
from docutils.statemachine import StringList

from sphinx import addnodes
from sphinx.pycode.parser import Parser


def get_enum_docstrings(enum):
    """Extract attribute docstrings from an enum.

    Attribute docstrings are not supported by the Python interpretter,
    however, Sphinx has developed their own parser which is how autodoc
    picks them up.

    This uses their parser to extract attribute docstrings for enum values.

    Returns:
        {enum.Value: docstring}

    """
    parser = Parser(getsource(enum))
    parser.parse()
    return {
        key: cleandoc(docstring)
        for (_, key), docstring in parser.comments.items()
    }


def get_obj_from_module(namespace):
    """Import and return a something from a Python module.

    Examples:
        >>> get_obj_from_module('os')  # doctest: +ELLIPSIS
        <module 'os' from ...>
        >>> get_obj_from_module('os.walk')  # doctest: +ELLIPSIS
        <function walk at ...>
        >>> get_obj_from_module('os.path.join')  # doctest: +ELLIPSIS
        <function join at ...>

    """
    head, tail = namespace.split('.'), []
    while head:
        try:
            module = import_module('.'.join(head))
        except ModuleNotFoundError:
            tail.insert(0, head.pop())
        else:
            ret = module
            for item in tail:
                ret = getattr(ret, item)
            return ret


class EnumValueAutoDoc(Directive):
    """Document enum values along with attribute docstrings."""

    has_content = True

    def run(self):
        if len(self.content) != 1:
            raise ValueError(
                f'Got too many content lines, expected one.\n{self.content}'
            )

        # import the enum
        enum = get_obj_from_module(self.content[0])

        # extract docstrings using the Sphinx parser
        docstrings = get_enum_docstrings(enum)

        # build ReST code to document the enum
        rst = []
        rst.extend(cleandoc(enum.__doc__).splitlines())
        rst.append('')
        for item in enum:
            rst.extend(
                [f'.. describe:: {item.value}']
                + (
                    [''] + [
                        f'   {line}'
                        for line in docstrings[item.name].splitlines()
                    ] + ['']
                    if item.name in docstrings
                    else ['']
                )
            )

        # return a node with the parsed ReST
        node = addnodes.desc()
        self.state.nested_parse(
            StringList(rst),
            self.content_offset,
            node
        )
        return [node]


def setup(app):
    app.add_directive('autoenumvalues', EnumValueAutoDoc)
