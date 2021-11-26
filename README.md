# Cylc Documentation

[![stable](https://img.shields.io/website?label=stable&up_message=live&url=https%3A%2F%2Fcylc.github.io%2Fcylc-doc%2Fstable%2Fhtml%2Findex.html)](https://cylc.github.io/cylc-doc/stable/html/index.html)
[![latest](https://img.shields.io/website?label=latest&up_message=live&url=https%3A%2F%2Fcylc.github.io%2Fcylc-doc%2Flatest%2Fhtml%2Findex.html)](https://cylc.github.io/cylc-doc/latest/html/index.html)
[![nightly](https://img.shields.io/website?label=nightly&labelColor=&up_message=live&url=https%3A%2F%2Fcylc.github.io%2Fcylc-doc%2Fnightly%2Fhtml%2Findex.html)](https://cylc.github.io/cylc-doc/nightly/html/index.html)

Documentation for the Cylc Workflow Engine and its software ecosystem.

## Writing

The documentation is written in ReStructuredText, for more information see:

* https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
* https://docutils.sourceforge.io/docs/user/rst/quickstart.html

We use the following convention for underlining headings:

```rest
Heading
=======

Sub Heading
-----------

Sub Sub Heading
^^^^^^^^^^^^^^^
```

ReStructuredText uses "natural indentation" where subsequent lines should follow
the indentation of previous lines e.g:

```rest
Bullet Points
=============

Indent subsequent lines two spaces:

* Foo
  bar
  baz.
* Pub.

Numbered Lists
==============

Indent subsequent lines three spaces:

1. Foo
   bar
   baz.
2. Pub.

Directives
==========

Indent subsequent lines three spaces:

.. directive:: argument

   content

Note there should be one blank line before the content.
```

Hyperlinks that are likely to be common between pages can be put in
``src/hyperlinks.rst.include`` where they are available to all pages.

Cylc configurations should be referenced using `:cylc:conf:`:

```rest
Tell Cylc what to run using :cylc:conf:`[runtime][<namespace>]script`.
```

Content from other Sphinx documented projects (Rose, Python, etc) can be linked
to via intersphinx.

We use a few custom Sphinx extensions, for details see
[cylc-sphinx-extensions](https://cylc.github.io/cylc-sphinx-extensions/).

## Development

[![test](https://github.com/cylc/cylc-doc/workflows/test/badge.svg?branch=master&event=push)](https://github.com/cylc/cylc-doc/actions?query=workflow%3Atest)
[![nightly](https://github.com/cylc/cylc-doc/workflows/nightly/badge.svg)](https://github.com/cylc/cylc-doc/actions?query=workflow%3Anightly)

```console
$ git clone git@github.com:cylc/cylc-doc.git cylc-doc
$ cd cylc-doc
$ pip install -e .
$ make html
```

## Testing

```console
# note: -W tells Sphinx to fail on warnings
$ make html linkcheck doctest SPHINXOPTS='-W'
```

## Deploying

**To document a new version of Cylc:**

* Create a tag with a name matching a released cylc-flow tag.
* Push it to `cylc/cylc-doc`.
* Trigger the `deploy` workflow against that tag.

**To update documentation for an existing version (post release):**

* Update the existing tag.
* Push it to `cylc/cylc-doc`.
* Trigger the `deploy` workflow against that tag.

**To remove old documentation:**

* Trigger the `undeploy` workflow against the relevant tag.

**To do any other weird or wonderful things:**

* Checkout `upstream/gh-pages`.
* Make your changes and add them to a new commit.
* Push to `upstream/gh-pages` (don't force push for ease of rollback).

> **Note:** All changes made to the `gh-pages` branch are non-destructive
  (i.e. no force pushing) so all changes can be undone.

  The `deploy` and `undeploy` actions are automations for convenience, however,
  everything can still be done by hand.

> **Warning:** When you remove an old version from the documentation the
  old version is still in the commit history. After a while we may wish to
  rebase-squeeze the `gh-pages` branch to reduce the size of the repo.

  This has not been automated on-purpose, though if it becomes a problem
  we could potentially setup a chron job to squash all but the last N commits.

## Nightly Builds

The `nightly` action builds `cylc-doc:master` against `cylc-flow:master`
and pushes the result up to `upstream/gh-pages`.

This action deletes its previous commits so the nightly build history is not
preserved and does not require housekeeping.

## Copyright and Terms of Use

[![License](https://img.shields.io/github/license/cylc/cylc-doc.svg?color=lightgrey)](https://github.com/cylc/cylc-doc/blob/master/LICENSE)

Copyright (C) 2008-<span actions:bind='current-year'>2021</span> NIWA & British Crown (Met Office) & Contributors.

Cylc is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

Cylc is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
Cylc.  If not, see [GNU licenses](http://www.gnu.org/licenses/).
