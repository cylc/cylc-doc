.. _cylc-broadcast:

Cylc Broadcast
--------------

The ``cylc broadcast`` command overrides task :cylc:conf:`[runtime]`
settings in a running scheduler. You can think of it as communicating
new configuration settings (including information via environment variables) to
selected upcoming tasks via the scheduler.

See ``cylc broadcast --help`` for detailed information.

Broadcast settings targeting a specific cycle point expire as the workflow
moves on. Otherwise they persist for lifetime of the run, and across restarts,
unless cleared with another invocation of the command.

.. seealso::

   :ref:`broadcast-tutorial`

.. TODO: document sub-workflows
