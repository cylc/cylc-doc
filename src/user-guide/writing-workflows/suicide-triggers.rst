
.. TAKEN OUT OF THE USER GUIDE FOR CYLC 8
   We made need to keep this as a reference for rare remaining use cases

.. _SuicideTriggers:

Suicide Triggers
^^^^^^^^^^^^^^^^

.. tutorial:: Suicide Trigger Tutorial <tut-cylc-suicide-triggers>

Suicide triggers take tasks out of the workflow. This can be used for automated
failure recovery. The following :cylc:conf:`flow.cylc` listing and accompanying
:term:`graph` show how to define a chain of failure recovery tasks that trigger
if they're needed but otherwise remove themselves from the workflow (you can run
the *AutoRecover.async* example workflow to see how this works). The dashed graph
edges ending in solid dots indicate suicide triggers, and the open arrowheads
indicate conditional triggers as usual.

.. Need to use a 'container' directive to get centered image with
   left-aligned caption (as required for code block text).

.. container:: twocol

   .. container:: caption

      *Automated failure recovery via suicide triggers*

      .. code-block:: cylc

          [meta]
              title = automated failure recovery
              description = """
                  Model task failure triggers diagnosis
                  and recovery tasks, which take themselves
                  out of the workflow if model succeeds. Model
                  post processing triggers off model OR
                  recovery tasks.
              """
          [scheduling]
              [[graph]]
                  R1 = """
                      pre => model
                      model:fail => diagnose => recover
                      model => !diagnose & !recover
                      model | recover => post
                  """
          [runtime]
              [[model]]
                  # UNCOMMENT TO TEST FAILURE:
                  # script = /bin/false

   .. container:: image

      .. _fig-suicide:

      .. figure:: ../../img/suicide.png
         :align: center


.. note::

   Multiple suicide triggers combine in the same way as other
   triggers, so this:

   .. code-block:: cylc-graph

      foo => !baz
      bar => !baz

   is equivalent to this:

   .. code-block:: cylc-graph

      foo & bar => !baz

   i.e. both ``foo`` and ``bar`` must succeed for
   ``baz`` to be taken out of the workflow. If you really want a task
   to be taken out if any one of several events occurs then be careful to
   write it that way:

   .. code-block:: cylc-graph

      foo | bar => !baz

.. warning::

   A word of warning on the meaning of "bare suicide triggers". Consider
   the following workflow:

   .. code-block:: cylc

      [scheduling]
          [[graph]]
              R1 = "foo => !bar"

   Task ``bar`` has a suicide trigger but no normal prerequisites
   (a suicide trigger is not a task triggering prerequisite, it is a task
   removal prerequisite) so this is entirely equivalent to:

   .. code-block:: cylc

      [scheduling]
          [[graph]]
              R1 = """
                  foo & bar
                  foo => !bar
              """

   In other words both tasks will trigger immediately, at the same time,
   and then ``bar`` will be removed if ``foo`` succeeds.

If an active task proxy (currently in the submitted or running states)
is removed from the workflow by a suicide trigger, a warning will be logged.


