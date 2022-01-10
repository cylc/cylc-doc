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
        autodoc_traits.py
"""
from sphinx.ext.autodoc import AttributeDocumenter
from sphinx.ext.autodoc import ClassDocumenter
from traitlets import TraitType
from traitlets import Undefined


class ConfigurableDocumenter(ClassDocumenter):
    """Specialized Documenter subclass for traits with config=True"""

    objtype = "configurable"
    directivetype = "class"

    def get_object_members(self, want_all):
        """Add traits with .tag(config=True) to members list"""
        check, members = super().get_object_members(want_all)
        get_traits = (
            self.object.class_own_traits
            if self.options.inherited_members
            else self.object.class_traits
        )
        trait_members = []
        for name, trait in sorted(get_traits(config=True).items()):
            # put help in __doc__ where autodoc will look for it
            trait.__doc__ = trait.help
            trait_members.append((name, trait))
        return check, trait_members


class TraitDocumenter(AttributeDocumenter):
    objtype = "trait"
    directivetype = "attribute"
    member_order = 1
    priority = 100

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return isinstance(member, TraitType)

    def add_directive_header(self, sig):
        default = self.object.get_default_value()
        if default is Undefined:
            default_s = ""
        else:
            default_s = repr(default)
        self.options.annotation = "c.{name} = {trait}({default})".format(
            name=self.format_name(),
            trait=self.object.__class__.__name__,
            default=default_s,
        )
        super().add_directive_header(sig)


def setup(app):
    app.add_autodocumenter(ConfigurableDocumenter)
    app.add_autodocumenter(TraitDocumenter)
