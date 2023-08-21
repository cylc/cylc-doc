.. _configuration-changes:

Configuration Changes at Cylc 8
===============================

Some configurations have moved or been renamed at Cylc 8.

The old configurations are now deprecated, but still supported.
These will be highlighted upon ``cylc validate`` after renaming ``suite.rc``
to ``flow.cylc``.

Because some workflows use Jinja2 or EmPy branches which may not be switched on at
the time of the initial ``cylc validate`` we have also provided
a script, :ref:`cylc lint -r 728 <cylc_lint_script>` to check for Cylc 7
syntax which may be deprecated.

There are some examples below of how to upgrade:


.. _7-to-8.graph_syntax:

Graph
-----

Cylc 7 had unnecessarily deep nesting of graph config sections:

.. code-block:: cylc

   [scheduling]
       initial cycle point = now
       [[dependencies]]
           [[[R1]]]
               graph = "prep => foo"
           [[[R/^/P1D]]]
               graph = "foo => bar => baz"

Cylc 8 cleans this up:

.. code-block:: cylc

   [scheduling]
       initial cycle point = now
       [[graph]]
           R1 = "prep => foo"
           R/^/P1D = "foo => bar => baz"


Fixing deprecation warnings
---------------------------

Take the following example ``flow.cylc`` file:

.. code-block:: cylc

   [cylc]
      UTC mode = True
   [scheduling]
       initial cycle point = 2000-01-01
       [[dependencies]]
           [[[R1]]]
               graph = foo => bar
   [runtime]
       [[foo, bar]]

This workflow will pass validation at Cylc 8, but will give warnings:

.. code-block:: console

   $ cylc validate .
   WARNING - deprecated items were automatically upgraded in "workflow definition"
   WARNING -  * (8.0.0) [cylc] -> [scheduler] - value unchanged
   WARNING - deprecated graph items were automatically upgraded in "workflow definition":
      * (8.0.0) [scheduling][dependencies][X]graph -> [scheduling][graph]X - for X in:
            R1
   Valid for cylc-8.0.0

The warnings explain what needs to be fixed. After making the following changes,
the workflow will validate without any warnings:

.. code-block:: diff

   -[cylc]
   +[scheduler]
        UTC mode = True
    [scheduling]
        initial cycle point = 2000-01-01
   -    [[dependencies]]
   -        [[[R1]]]
   -            graph = foo => bar
   +    [[graph]]
   +        R1 = foo => bar
    [runtime]
        [[foo, bar]]

.. tip::

   Later Cylc releases will not be able to upgrade obsolete Cylc 7
   configurations. It's a good idea to address warnings as part of routine
   workflow review and maintenance to avoid problems later on.


Platforms
---------

.. seealso::

   - :ref:`Platforms at Cylc 8. <majorchangesplatforms>`
   - :ref:`System admin's guide to writing platforms. <AdminGuide.PlatformConfigs>`

At Cylc 7, job hosts were defined to indicate where a job should run.
At Cylc 8, this has been replaced by Platforms.

.. code-block:: diff

    [runtime]
        [[foo]]
   -        [[[job]]]
   -            batch system = slurm
   -        [[[remote]]]
   -            host = hpc1.login.1
   +        platform = hpc1

For a comprehensive list of valid configuration, see: :ref:`workflow-configuration`
and :ref:`global-configuration`.
