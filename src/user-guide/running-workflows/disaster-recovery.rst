.. TODo - Re-write for Cylc 8


.. _Disaster Recovery:

Disaster Recovery
-----------------

If a run directory gets deleted or corrupted, the options for recovery
are:

- restore the run directory from back-up, and restart the workflow
- re-install from source, and warm start from the beginning of the
  current cycle point

A warm start (see :ref:`Warm Start`) does not need the workflow database, but it
could re-run a significant number of tasks that had already completed.

To restart the workflow, the critical Cylc files that must be restored are:

.. code-block:: sub

   # On the workflow host:
   ~/cylc-run/WORKFLOW-NAME/
       flow.cylc  # installed workflow configuration
       log/db  # public workflow DB (can just be a copy of the private DB)
       log/rose-suite-run.conf  # (needed to restart a Rose workflow)
       .service/db  # private workflow DB
       .service/source -> PATH-TO-WORKFLOW-DIR  # symlink to workflow source

   # On job hosts (if no shared filesystem):
   ~/cylc-run/WORKFLOW-NAME/
       log/job/CYCLE-POINT/TASK-NAME/SUBMIT-NUM/job.status

.. note::

   This discussion does not address restoration of files generated and
   consumed by task jobs at run time. How workflow data is stored and recovered
   in your environment is a matter of workflow and system design.

In short, you can simply restore the workflow :term:`service directory`, the
:term:`workflow log directory`, and the :cylc:conf:`flow.cylc` file that is the
target of the symlink in the service directory. The :term:`service directory`
and :term:`workflow log directory` will come with extra files that aren't strictly
needed for a restart, but that doesn't matter - although depending on your log
housekeeping the ``log/job`` directory could be huge, so you might want to be
selective about that. (Also in a Rose workflow, the ``flow.cylc`` file does not
need to be restored if you restart with ``rose suite-run`` - which re-installs
workflow source files to the run directory).

The public DB is not strictly required for a restart; if it is absent,
the :term:`scheduler` will recreate it.

The job status files are only needed if the workflow state at last shutdown
contained active tasks that now need to be polled to determine what happened to them
while the workflow was down. Without them, polling will fail and those tasks will
need to be manually set to the correct state.

.. warning::

   It is not safe to copy or rsync a potentially-active sqlite DB - the copy
   might end up corrupted. It is best to stop the workflow before copying
   a DB, or else write a back-up utility using the
   `official sqlite backup API <https://www.sqlite.org/backup.html>`_.
