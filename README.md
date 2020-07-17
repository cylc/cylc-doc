# Cylc Documentation

![test](https://github.com/cylc/cylc-doc/workflows/test/badge.svg?branch=master&event=push)

Documentation for the Cylc Workflow Engine and its software ecosystem.

## Development

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
