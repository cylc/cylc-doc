.. _cylc_7_compat_mode:

Cylc 7 Compatibility Mode
=========================

.. admonition:: Does This Change Affect Me?
   :class: tip

   This will affect you if you want to run Cylc 7 (``suite.rc``) workflows
   using Cylc 8.

Overview
--------

Cylc 8 can run most Cylc 7 workflows "as is".
The ``suite.rc`` filename triggers a backward compatibility mode in which:

- :term:`implicit tasks <implicit task>` are allowed by default

  - (unless a ``rose-suite.conf`` file is found in the :term:`run directory`
    for consistency with ``rose suite-run`` behaviour)
  - (Cylc 8 does not allow implicit tasks by default)

- :term:`cycle point time zone` defaults to the local time zone

  - (Cylc 8 defaults to UTC)

- waiting tasks are pre-spawned to mimic the Cylc 7 scheduling algorithm and
  stall behaviour, and these require
  :term:`suicide triggers <suicide trigger>`
  for alternate :term:`graph branching`

  - (Cylc 8 spawns tasks on demand, and suicide triggers are not needed for
    branching)

- only ``succeeded`` task outputs are :ref:`*required* <User Guide Required Outputs>`,
  meaning the scheduler will retain tasks that do not succeed as incomplete

  - (in Cylc 8, **all** outputs are *required* unless marked as
    :ref:`*optional* <User Guide Optional Outputs>` by the new ``?`` syntax)


.. _compat_required_changes:

Required Changes
----------------

Providing your Cylc 7 workflow does not use syntax that was deprecated at Cylc 7,
you may be able to run it using Cylc 8 without any modifications while in
compatibility mode.

First, run ``cylc validate`` **with Cylc 7** on your ``suite.rc`` workflow
to check for deprecation warnings and fix those before validating with Cylc 8.
See :ref:`below <compat.eg.c7val>` for an example.

.. warning::

   ``cylc validate`` operates on the processed ``suite.rc``, which
   means it will not detect any deprecated syntax that is inside a
   currently-unused Jinja2/EmPy ``if...else`` branch.

Some workflows may require modifications to either upgrade to Cylc 8 or make
interoperable with Cylc 8 backward compatibility mode. Read on for more details.


Cylc commands in task scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check for any use of Cylc commands in task scripting. Some Cylc 7 commands
have been removed and some others now behave differently.
However, ``cylc message`` and ``cylc broadcast`` have *not* changed.
See the :ref:`full list of command line interface changes<MajorChangesCLI>`
and see :ref:`below <compat.eg.cylc-commands>` for an example.


Python 2 to 3
^^^^^^^^^^^^^

Whereas Cylc 7 runs using Python 2, Cylc 8 runs using Python 3. This affects:
- modules imported in Jinja2
- Jinja2 filters, tests and globals
- custom xtrigger functions

Note that task scripts are not affected - they run in an independent
environment.

See :ref:`py23` for more information and examples of how to implement
interoperability if your workflows extend Cylc or Jinja2 with custom Python scripts.


Other caveats
^^^^^^^^^^^^^

- Cylc 8 cannot *restart* a partially completed Cylc 7 workflow in-place. If
  possible, complete the run with Cylc 7. Otherwise, see
  :ref:`compat_continuing_c7_with_c8`.

- Cylc 8 only transfers certain files and directories by default during
  remote installation. See :ref:`728.remote-install` for more information.

- Cylc 8 does not support
  :ref:`excluding/including tasks at start-up<MajorChangesExcludingTasksAtStartup>`.
  If your workflow used this old functionality, it may have been used in
  combination with the ``cylc insert`` command (which has been removed from
  Cylc 8) and ``cylc remove`` (which still exists but is much less needed).

- Cylc 8 does not support :ref:`specifying remote usernames <728.remote_owner>`
  using :cylc:conf:`flow.cylc[runtime][<namespace>][remote]owner`.


Examples
--------

.. _compat.eg.c7val:

Validating with Cylc 7
^^^^^^^^^^^^^^^^^^^^^^

Consider this configuration:

.. code-block:: cylc
   :caption: ``suite.rc``

   [scheduling]
       initial cycle point = 11000101T00
       [[dependencies]]
           [[[R1]]]
               graph = task

   [runtime]
       [[task]]
           pre-command scripting = echo "Hello World"

Running ``cylc validate`` at **Cylc 7** we see that the
workflow is valid, but we are warned that ``pre-command scripting``
was replaced by ``pre-script`` at 6.4.0:

.. code-block:: console
   :caption: Cylc 7 validation

   $ cylc validate .
   WARNING - deprecated items were automatically upgraded in 'suite definition':
   WARNING -  * (6.4.0) [runtime][task][pre-command scripting] -> [runtime][task][pre-script] - value unchanged
   Valid for cylc-7.8.7

.. note::

   **Cylc 7** has handled this deprecation for us, but at **Cylc 8** this
   workflow will fail validation.

   .. code-block:: console
      :caption: Cylc 8 validation

      $ cylc validate .
      IllegalItemError: [runtime][task]pre-command scripting

You must change the configuration yourself. In this case:

.. code-block:: diff

   -     pre-command scripting = echo "Hello World"
   +     pre-script = echo "Hello World"

Validation will now succeed.


.. _compat.eg.cylc-commands:

Cylc commands in task scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You might have a task script that calls a Cylc command like so:

.. code-block:: cylc

   [runtime]
       [[foo]]
           script = cylc hold "$CYLC_SUITE_NAME"

The ``cylc hold`` command has changed in Cylc 8. It is now used for holding
tasks only; use ``cylc pause`` for entire workflows.
(Additionally, ``$CYLC_SUITE_NAME`` is deprecated in favour of
``$CYLC_WORKFLOW_ID``, though still supported.)

In order to make this interoperable, so that you can run it with both Cylc 7
and Cylc 8 backward compatibility mode, you could do something like this
in the bash script:

.. code-block:: cylc

   [runtime]
       [[foo]]
           script = """
               if [[ "${CYLC_VERSION:0:1}" == 7 ]]; then
                   cylc hold "$CYLC_SUITE_NAME"
               else
                   cylc pause "$CYLC_WORKFLOW_ID"
               fi
           """

Note this logic (and the ``$CYLC_VERSION`` environment variable) is executed
at runtime on the :term:`job host`.

Alternatively, you could use :ref:`Jinja` like so:

.. code-block:: cylc

   [runtime]
       [[foo]]
           {% if CYLC_VERSION is defined and CYLC_VERSION[0] == '8' %}
               script = cylc pause "$CYLC_WORKFLOW_ID"
           {% else %}
               script = cylc hold "$CYLC_SUITE_NAME"
           {% endif %}

Note this logic (and the ``CYLC_VERSION`` Jinja2 variable) is executed locally
prior to Cylc parsing the workflow configuration.


Renaming to ``flow.cylc``
-------------------------

When your workflow runs successfully in backward compatibility mode, it is
ready for renaming ``suite.rc`` to ``flow.cylc``. Doing this will turn off
backward compatibility mode, and validation in Cylc 8 will show
deprecation warnings.

.. seealso::

   :ref:`configuration-changes`

.. important::

   More complex workflows (e.g. those with suicide triggers) may
   fail validation once backward compatibility is off - see
   :ref:`728.optional_outputs`
