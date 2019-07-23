# THIS FILE IS PART OF THE CYLC SUITE ENGINE.
# Copyright (C) 2008-2019 NIWA & British Crown (Met Office) & Contributors.
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

from distutils.spawn import find_executable as which
import sys
import os
from cylc.flow import __version__ as CYLC_VERSION


# -- General configuration ------------------------------------------------

# minimal Sphinx version required.
needs_sphinx = '1.5.3'

# Sphinx extension module names.
sys.path.append(os.path.abspath('ext'))  # path to custom extensions.
extensions = [
    # sphinx built-in extensions
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.graphviz',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    # sphinx user community extensions
    'hieroglyph',
    'sphinx_rtd_theme',
    # custom project extensions (located in ext/)
    'cylc_lang',
    'minicylc',
    'practical',
    'sub_lang',
    'hieroglyph_patch'  # https://github.com/nyergler/hieroglyph/issues/148
]

rst_epilog = open('hyperlinks.rst.include', 'r').read()

# Select best available SVG image converter.
for svg_converter, extension in [
        ('rsvg', 'sphinxcontrib.rsvgconverter'),
        ('inkscape', 'sphinxcontrib.inkscapeconverter')]:
    if which(svg_converter):
        try:
            __import__(extension)
        except (AssertionError, ImportError):
            # converter or extension not available
            pass
        else:
            extensions.append(extension)
            break
else:
    # no extensions or converters available, fall-back to default
    # vector graphics will be converted to bitmaps in all documents
    extensions.append('sphinx.ext.imgconverter')

# Add any paths that contain templates.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Cylc'
copyright = '2008-2019 NIWA & British Crown (Met Office) & Contributors'

# Versioning information. Sphinx advises version strictly meaning X.Y.
version = '.'.join(CYLC_VERSION.split('.')[:2])  # The short X.Y version.
release = CYLC_VERSION  # The full version, including alpha/beta/rc tags.

intersphinx_mapping = {
    'rose': (
        'http://metomi.github.io/rose/doc/html', None
    )
}

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'autumn'

# Enable automatic numbering of any captioned figures, tables & code blocks.
numfig = True
numfig_secnum_depth = 0

# Global configuration for graphviz diagrams.
graphviz_output_format = 'svg'
graphviz_dot_args = ['-Gfontname=sans', '-Gbgcolor=none',
                     '-Nfontname=sans']


# -- Options for HTML output ----------------------------------------------

# Theme
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': True,
    'navigation_depth': 4
}
html_logo = "img/cylc-logo-white.svg"
html_favicon = "img/cylc-favicon.ico"  # sphinx specifies .ico format
html_show_sphinx = False
html_show_copyright = True
html_js_files = [
    'js/cylc.js'
]
html_css_files = [
    'css/cylc.css'
]

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    '**': [
        'globaltoc.html',
        'searchbox.html',
        'sourcelink.html',
        'versions.html'
    ],
}

html_static_path = ['_static']

# Disable timestamp otherwise inserted at bottom of every page.
html_last_updated_fmt = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'cylcdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
}

# Title for the cylc documentation section
CYLC_DOC_TITLE = 'Cylc Documentation'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    ('index', 'cylc.tex', CYLC_DOC_TITLE, copyright, 'manual'),
]

# Image file to place at the top of the title page.
latex_logo = "img/cylc-logo-greyscale.svg"

# If true, show URL addresses after external links.
latex_show_urls = "footnote"


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'cylc', CYLC_DOC_TITLE, copyright, 1),
]

# If true, show URL addresses after external links.
man_show_urls = True


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ('index', 'cylc', CYLC_DOC_TITLE, copyright, 'cylc', project,
     'Miscellaneous'),
]

# How to display URL addresses.
texinfo_show_urls = 'footnote'
