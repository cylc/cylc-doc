.. _Workflow Run Databases:

Workflow Run Databases
----------------------

Schedulers maintain two ``sqlite`` databases to record
information on run history:

.. code-block:: console

   $HOME/cylc-run/WORKFLOW-NAME/log/db  # public workflow DB
   $HOME/cylc-run/WORKFLOW-NAME/.service/db  # private workflow DB

The private DB is for use only by the :term:`scheduler`. The identical
public DB is provided for use by external commands such as
``cylc workflow-state``, and ``cylc report-timings``.
If the public DB gets locked for too long by
an external reader, the :term:`scheduler` will eventually delete it and
replace it with a new copy of the private DB, to ensure that both correctly
reflect the workflow state.

You can interrogate the public DB with the ``sqlite3`` command line tool,
the ``sqlite3`` module in the Python standard library, or any other
sqlite interface.

.. code-block:: console

   $ sqlite3 ~/cylc-run/foo/log/db << _END_
   > .headers on
   > select * from task_events where name is "foo";
   > _END_
   name|cycle|time|submit_num|event|message
   foo|1|2017-03-12T11:06:09Z|1|submitted|
   foo|1|2017-03-12T11:06:09Z|1|output completed|started
   foo|1|2017-03-12T11:06:09Z|1|started|
   foo|1|2017-03-12T11:06:19Z|1|output completed|succeeded
   foo|1|2017-03-12T11:06:19Z|1|succeeded|

The diagram shown below contains the database tables, their columns,
and how the tables are related to each other. For more details on how
to interpret the diagram, refer to the
`Entity–relationship model Wikipedia article <https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model>`_.

.. cylc-db-graph::
   :align: center
