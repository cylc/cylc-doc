.. _conda environments:

Conda Environments
==================

Cylc consists of multiple components.

This Conda environment will provide you with the "recommended" installation of
all components:

.. literalsubinclude:: envs/cylc-all.yml
   :language: YAML
   :substitutions:

The following sections outline alternatives for finer control over installation.


Cylc Flow
---------

The simplest Cylc installation consists only of `Cylc Flow`_:

.. literalsubinclude:: envs/cylc-flow.yml
   :language: YAML
   :substitutions:

.. tip::

   We suggest installing `Cylc Flow`_ at a "minor" version (e.g. ``8.1`` rather
   than ``8.1.2``) to pick up the latest "mainteinance" release.

If you do not specify your Python version you will be provided with the most
recent compatible one.

If you are installing Cylc on multiple machines across a network it is
advisable to keep the Python versions consistent.

You can do this by adding Python into the environment at a particular version:

.. literalsubinclude:: envs/cylc-flow-with-python.yml
   :language: YAML
   :substitutions:

`Cylc Flow`_ provides a cut-down package containing only the bare essentials
called ``cylc-flow-base``.

This may be useful for installing onto job hosts where client-facing extra
features are not of interest:

.. literalsubinclude:: envs/cylc-flow-base.yml
   :language: YAML
   :substitutions:


Cylc UIServer
-------------

The default `Cylc UIServer`_ package comes with `Jupyter Hub`_ and the
`Configurable HTTP Proxy`_ (required by `Jupyter Hub`_) bundled:

.. literalsubinclude:: envs/cylc-uiserver.yml
   :language: YAML
   :substitutions:

.. tip::

   We suggest *not* specifying the version of other Cylc components to
   (i.e. `Cylc UIServer`_ and `Cylc Rose`_). This will pick up the most recent
   version compatible with the specified `Cylc Flow`_ version.

`Jupyter Hub`_ is only required for multi-user setups, the `Cylc UIServer`_
can be run as a standalone application.

To exclude `Jupyter Hub`_ from the installation use ``cylc-uiserver-base``:

.. literalsubinclude:: envs/cylc-uiserver-without-jupyterhub.yml
   :language: YAML
   :substitutions:

If you want to use `Jupyter Hub`_ with an alternative proxy use
``cylc-uiserver-hub-base`` (this depends on ``jupyterhub-base``, see the
`Jupyter Hub`_ documentation for details):

.. literalsubinclude:: envs/cylc-uiserver-with-traefik-proxy.yml
   :language: YAML
   :substitutions:


Cylc Rose
---------

For working with Rose add ``metomi-rose`` and ``cylc-rose`` (the bridge
between Cylc & Rose):

.. literalsubinclude:: envs/cylc-rose.yml
   :language: YAML
   :substitutions:

We will look at providing more installation options for Rose in the near
future.


Adding Cylc To Your Conda Package
---------------------------------

If you want to publish a package (e.g. to Conda Forge) that depends on Cylc,
consider using the minimal package (e.g. ``cylc-flow-base``) as a dependency
to allow the installer to maintain flexibility over the installation.


Working With Other Conda Channels
---------------------------------

Cylc projects are published to Conda Forge and the above environments install
all dependencies from Conda Forge.

If you want to install other dependencies (e.g. Python), from other channels
(e.g. Anaconda), list the dependency explicitly and place the channel *above*
the Conda Forge channel.

.. literalsubinclude:: envs/cylc-flow-anaconda.yml
   :language: YAML
   :substitutions:
