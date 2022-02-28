.. _configuration-changes:

Configuration Changes at Cylc 8
===============================

Some configurations have moved or been renamed at Cylc 8.

The old configurations are now deprecated, but still supported. These will be highlighted upon
``cylc validate``.

There are some examples below of how to upgrade:

.. _7-to-8.graph_syntax:

Graph
-----
Cylc 7 had unnecessarily deep nesting of graph config sections:

.. code-block:: cylc

   [scheduling]
      initial cycle point = now
      [[dependencies]]  # Deprecated Cylc 7
          [[[R1]]]
              graph = "prep => foo"
          [[[R/^/P1D]]]
              graph = "foo => bar => baz"

Cylc 8 cleans this up:

.. code-block:: cylc

   [scheduling]
      initial cycle point = now
      [[graph]]  # Cylc 8
          R1 = "prep => foo"
          R/^/P1D = "foo => bar => baz"

Platforms
---------
.. seealso::

   - :ref:`Platforms at Cylc 8. <majorchangesplatforms>`
   - :ref:`System admin's guide to writing platforms. <AdminGuide.PlatformConfigs>`

At Cylc 7 job hosts were defined to indicate where a job should run, at Cylc 8
use Platforms.

.. code-block:: diff

     [runtime]
        [[model]]
   -        [[[remote]]]
   -            host = hpc1.login.1
   +        platform = hpc1

For a comprehensive list of valid configuration, see: :ref:`workflow-configuration`
and :ref:`global-configuration`.