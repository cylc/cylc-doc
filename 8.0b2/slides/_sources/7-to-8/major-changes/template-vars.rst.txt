Template Variables
==================

.. admonition:: Does This Change Affect Me?
   :class: tip

   Read this section if you set Cylc template variables on the command line
   using the ``-s``, ``--set`` or ``-set-file`` options.

   This does *not* affect the Rose ``jinja2:suite.rc`` and
   ``empy:suite.rc`` variables set using the ``-S`` option to the
   ``rose suite-run`` command.


Overview
--------

Template variables are passed to :ref:`Jinja2 <Jinja>` or
:ref:`EmPy <User Guide EmPy>` for parsing the workflow definition in the
:cylc:conf:`flow.cylc` file.

In Cylc 7 template variables could only be strings, in Cylc 8 they can be any
valid Python literal including numbers, booleans, and lists.


Changes
-------

Strings must be explicitly quoted i.e. ``key="value"`` rather than ``key=value``.


Example
-------

.. rubric:: Setting template variables on the command line:

.. code-block:: bash

   # Cylc 7
   cylc run <suite> -s 'FOO=abc'
   # Cylc 8
   cylc play <flow> -s 'FOO="abc"'


.. rubric:: Setting template variables in a "set file" (using ``--set-file``):

.. code-block:: python

   # Cylc 7
   FOO = abc
   BAR = bcd

   # Cylc 8
   FOO = "abc"
   BAR = "bcd"


New Features
------------

Template variables can now be any valid Python literals e.g:

.. code-block:: python

   "string"   # string
   123        # integer
   12.34      # float
   True       # boolean
   None       # None type
   [1, 2, 3]  # list
   (1, 2, 3)  # tuple
   {1, 2, 3}  # set
   {"a": 1, "b": 2, "c": 3}  # dictionary

See :ref:`jinja2-template-variables` for more information.
