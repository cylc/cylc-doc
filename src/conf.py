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

from distutils.spawn import find_executable as which
import os
from pathlib import Path
import sys

from cylc.flow import __version__ as CYLC_VERSION
from cylc.flow.workflow_files import WorkflowFiles

sys.path.append(os.path.abspath('lib'))  # path to lib.

from cylc_release import CYLC_RELEASE

# -- General configuration ------------------------------------------------

# Sphinx extension module names.
sys.path.append(os.path.abspath('ext'))  # path to custom extensions.
extensions = [
    # sphinx built-in extensions
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.graphviz',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.spelling',
    # sphinx user community extensions
    'hieroglyph',
    'sphinx_rtd_theme',
    # custom project extensions (located in ext/)
    'autodoc_traits',  # autodoc uiserver traitlets
    'database_diagram',
    'autodoc_enum_values',
    # cylc-sphinx-extensions
    'cylc.sphinx_ext.cylc_lang',
    'cylc.sphinx_ext.diff_selection',
    'cylc.sphinx_ext.grid_table',
    'cylc.sphinx_ext.hieroglyph_addons',
    'cylc.sphinx_ext.minicylc',
    'cylc.sphinx_ext.practical',
    'cylc.sphinx_ext.rtd_theme_addons',
    'cylc.sphinx_ext.sub_lang',
    'cylc.sphinx_ext.literal_sub_include'
]

# Can define substitutions in prolog/epilog:
rst_prolog = f"""
.. |reserved_filenames| replace:: ``{'``, ``'.join(WorkflowFiles.RESERVED_NAMES)}``
"""
rst_epilog = open('hyperlinks.rst.include', 'r').read()

default_role = 'cylc:conf'

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
__copyright_year = 2023  # NOTE: this is automatically set by GH Actions
copyright = (
    f'2008-{__copyright_year} NIWA & British Crown (Met Office) & Contributors'
)

# Versioning information.
# NOTE: Sphinx considers version/release the other way around to us
release = CYLC_VERSION  # full version e.g. "8.0.0"
version = CYLC_RELEASE  # short version (for pinning / display) e.g. "8.0"

# Autosummary opts (for auto generation of docs from source code).
autosummary_generate = True
autosummary_generate_overwrite = True
autosummary_imported_members = False

# Mapping to other Sphinx projects we want to import references from.
intersphinx_mapping = {
    'rose': (
        'http://metomi.github.io/rose/2.0.0/html', None
    ),
    'python': (
        'https://docs.python.org/3/', None
    ),
    'jupyter_server': (
        'https://jupyter-server.readthedocs.io/en/latest/', None
    )
}

nitpick_ignore = [
    # This class appears in documented type-hints but is not documented in the
    # Python docs so fails build.
    ('py:class', 're.Pattern')
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'autumn'

# Global configuration for graphviz diagrams.
graphviz_output_format = 'svg'
graphviz_dot_args = ['-Gfontname=sans', '-Gbgcolor=none',
                     '-Nfontname=sans']

linkcheck_ignore = [
    # linkcheck has trouble handling RH readme pages
    r'https://github.com/metomi/isodatetime.*#.*'
]

nitpick_ignore_regex = [
    # intersphinx has trouble with pyzmq classes:
    ('py:class', 'zmq\.asyncio\.\w+')
]

# -- Options for Slides output ----------------------------------------------

slide_theme = 'single-level'
slide_link_to_html = True
slide_theme_options = {'custom_css': 'css/slides-custom.css'}


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

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    '**': [
        'globaltoc.html',
        'searchbox.html',
        'sourcelink.html',
        'versions.html'
    ],
}

# Values to pass into the templating context. Can be overridden using the
# sphinx-build opt `-A name=value` (add to SPHINXOPTS if using make).
html_context = {
    'sidebar_version_name': None,  # override name in version picker
}

html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = ['css/custom.css']

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

# Substitutions (e.g. |version|) to make when using literalsubinclude
literal_sub_include_subs = {
    'version': version,
    'release': release,
}

# Settings for spelling checks
# Proper nouns are words where we want to explicitly set the case, so
# include acronyms and proper names where we might want to explicitly set
# case lower, for example if we use it in scripts (e.g. "conda").
spelling_lang = 'en_NZ'
# for x in $(cat src/dictionaries/words);do echo ${x^};
# done > src/dictionaries/sentence_case
spelling_word_list_filename = [
    'dictionaries/words',
    'dictionaries/proper_nouns',
    'dictionaries/sentence_case'
]
spelling_warning = True
spelling_verbose = True

dictionaries = Path.cwd() / 'dictionaries'
wordsfile = dictionaries / 'words'
sentence_case_file = dictionaries / 'sentence_case'

# Sort wordlist:
words = wordsfile.read_text().split('\n')
words = [w for w in sorted(words) if w]
wordsfile.write_text('\n'.join(words) + '\n')

# Create sentence case versions of wordlist:
sentence_case = [word.capitalize() for word in words]
sentence_case_file.write_text('\n'.join(sentence_case) + '\n')
