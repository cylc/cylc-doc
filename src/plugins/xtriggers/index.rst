Xtrigger Plugins
======================================

Xtrigger plugins allow you to install and use xtriggers without them being
in your ``CYLC_PYTHONPATH``.


Built In Plugins
----------------

Cylc Flow provides the following xtriggers.

.. autosummary::
   :toctree: built-in
   :template: docstring_only.rst

   cylc.flow.xtriggers.echo
   cylc.flow.xtriggers.workflow_state
   cylc.flow.xtriggers.xrandom

.. Note: Autosummary generates files in this directory, these are cleaned
         up by `make clean`.

Developing ``xtrigger`` plugins
-------------------------------

Cylc uses entry points registered by setuptools to search for xtrigger
plugins.

Example
^^^^^^^

Plugins are registered by registering them with the ``cylc.xtriggers``
entry points. Each xtrigger is registered individually.

.. code-block:: ini
   :caption: ``setup.cfg``

   [options.entry_points]
       cylc.xtriggers =
           foo = my_package.foo:foo
           bar = my_package.foo:bar
           baz = my_package.baz:baz

.. code-block:: toml
   :caption: ``pyproject.toml``

   [project.entry-points."cylc.xtriggers"]
   foo = my_package.foo:foo
   bar = my_package.foo:bar
   baz = my_package.baz:baz

