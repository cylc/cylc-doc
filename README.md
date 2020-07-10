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

To document a new version of Cylc:

* Create a tag with a name matching a released cylc-flow tag.
* Push it upstream.
* The docs will auto build and deploy.

To update documentation for an existing version (post release):

* Update the existing tag.
* Push it upstream.
* The docs will auto build and deploy.

To remove old documentation:

* Checkout the gh-pages branch.
* `git rm doc/<version>`
* `git commit -m 'remove: <version>`
* `git push upstream gh-pages`
