#!/usr/bin/env python
# coding=utf-8

# THIS FILE IS PART OF THE CYLC SUITE ENGINE.
# Copyright (C) 2008-2018 NIWA & British Crown (Met Office) & Contributors.
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

from distutils.errors import DistutilsExecError
from os.path import join
from shutil import move, rmtree
from setuptools import setup
from sphinx.setup_command import BuildDoc


VERSION = "0.0.1"


class MakeDocs(BuildDoc):
    """Port of old `cylc-make-docs`. Removed in #2989.

    This class extends the Sphinx command class for setuptools. With
    a difference that it tries to mimic the behaviour of the previous
    `cylc-make-docs`.

    So first it will execute `make-commands.sh`, which builds the
    commands help information, in the appendices.

    Then, instead of calling one builder, this class will call the
    builder fot he single HTML, and also the builder for the multiple
    HTML documentation.

    Finally, one more tweak in this class is to move the doctrees
    folder (in the same level as the documentation) to within the
    documentation folder, named `.doctrees`, as before with
    `cylc-make-docs`.
    """

    def run(self):  # type: () -> None
        try:
            self.spawn(["./doc/src/custom/make-commands.sh"])
        except DistutilsExecError as exc:
            self.warn("Failed to run make-commands.sh")
            raise exc
        self.do_run("html", "built-sphinx")
        self.do_run("singlehtml", "built-sphinx-single")

    def do_run(self, builder: str, output_dir: str):
        """
        Args:
            builder (str): name of the Sphinx builder
            output_dir (str): directory to write the documentation produced
        """
        self.builder = builder
        self.builder_target_dirs = [
            (builder, join(self.build_dir, output_dir))]
        super().run()
        # move doctrees to $build_dir/.doctrees
        correct_doctrees = join(self.builder_target_dirs[0][1],
                                ".doctrees")
        rmtree(correct_doctrees, ignore_errors=True)
        move(self.doctree_dir, correct_doctrees)


cmdclass = {}
cmdclass["build_sphinx"] = MakeDocs


install_requires = [
    'sphinx==2.0.*',
    'cylc-flow==8.0a0',
]


setup(
    name='Cylc Documentation',
    version=VERSION,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    cmdclass=cmdclass,
    install_requires=install_requires,
    project_urls={
        "Documentation": "https://cylc.github.io/documentation.html",
        "Source": "https://github.com/cylc/cylc-doc",
        "Tracker": "https://github.com/cylc/cylc-doc/issues"
    }
)
