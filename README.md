# Cylc Documentation

[![Build Status](https://travis-ci.org/cylc/cylc-doc.svg?branch=master)](https://travis-ci.org/cylc/cylc-doc)

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
