Xtrigger Plugins
======================================

.. versionadded:: 8.3

   Xtrigger plugins allow you to install and use
   :ref:`xtriggers <Section External Triggers>` without them being
   in ``<workflow-dir>/lib/python/`` or ``$CYLC_PYTHONPATH``.

.. seealso::

   * :ref:`Built-in Clock Triggers`
   * :ref:`Built-in Workflow State Triggers`
   * :ref:`Built-in Toy Xtriggers`


.. _developing.xtrigger.plugins:

Developing ``xtrigger`` plugins
-------------------------------

Cylc uses the ``cylc.xtriggers`` entry point registered by setuptools to search
for xtrigger plugins. Each xtrigger is registered individually.

Example
^^^^^^^

Consider a package called ``my_package`` with the following structure:

.. code-block:: python
   :caption: ``my_package/foo.py``

   def foo():
       ...

   def bar():
       ...

.. code-block:: python
   :caption: ``my_package/baz.py``

   def baz():
       ...

These xtriggers can be registered in the package's ``setup.cfg`` or
``pyproject.toml`` file.

.. code-block:: ini
   :caption: ``setup.cfg``

   [options.entry_points]
   cylc.xtriggers =
       foo = my_package.foo
       bar = my_package.foo
       baz = my_package.baz

.. code-block:: toml
   :caption: ``pyproject.toml``

   [project.entry-points."cylc.xtriggers"]
   foo = "my_package.foo"
   bar = "my_package.foo"
   baz = "my_package.baz"

.. tip::

   It is recommended to implement only one xtrigger per module. This allows
   you to write a ``validate`` function for each xtrigger - see
   :py:mod:`cylc.flow.xtriggers.xrandom` for an example.
