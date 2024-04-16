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

https://github.com/jupyterhub/autodoc-traits/
    autodoc_traits.py

BSD 3-Clause License

Copyright (c) Project Jupyter Contributors
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from typing import List, Tuple

from sphinx.ext.autodoc import (
    AttributeDocumenter, ClassDocumenter, ObjectMember
)
from traitlets import TraitType
from traitlets import Undefined


class ConfigurableDocumenter(ClassDocumenter):
    """Specialized Documenter subclass for traits with config=True"""

    objtype = "configurable"
    directivetype = "class"

    def get_object_members(
        self, want_all: bool
    ) -> Tuple[bool, List[ObjectMember]]:
        """Add traits with .tag(config=True) to members list"""
        check, _ = super().get_object_members(want_all)
        if self.options.inherited_members:
            get_traits = self.object.class_own_traits
        else:
            get_traits = self.object.class_traits
        trait_members = [
            ObjectMember(name, trait, docstring=trait.help)
            for name, trait in sorted(get_traits(config=True).items())
        ]
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
