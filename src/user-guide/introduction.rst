Introduction
============


What is a Workflow?
-------------------

.. epigraph::

   A workflow consists of an orchestrated and repeatable pattern of business
   activity enabled by the systematic organization of resources into processes
   that transform materials, provide services, or process information.

   -- Wikipedia


.. tutorial:: What is a Workflow? <cylc-what-is-a-workflow>


What is Cylc?
-------------

Cylc (pronounced silk) is a workflow engine, a system that automatically
executes tasks according to schedules and dependencies.

In a Cylc workflow each step is an application: an executable command, script,
or program. Cylc runs each task as soon as it is appropriate to do so.


.. tutorial:: What is Cylc? <cylc-what-is-cylc>


Cylc and Cycling Workflows
--------------------------

A *cycling workflow* is a repetitive process involving many interdependent
tasks. Cylc tasks wrap arbitrary applications: executable commands,
scripts, or programs. Example use cases include:

- Processing many similar datasets, through a pipeline or graph of tasks
- Forecasting systems that generate new forecasts at regular intervals
- Splitting a long model run and associated processing tasks into many smaller runs
- Iterative tuning of model parameters by model, processing, and validation tasks

Cycling systems were traditionally managed by repeat-running the single-cycle
workflow, finishing each new cycle before starting the next. Sometimes, however,
it can be much more efficient to run multiple cycles at once. Even in real time
forecasting systems that normally have a gap between cycles waiting on new
data, this can greatly speed catch up from delays or downtime. But it can't
be done if the workflow manager has a global loop that handles only one cycle
at a time and does not understand any intercycle dependence that may be present.

.. important::

   Cylc handles inter- and intra-cycle dependence equally, and it unrolls the
   cycle loop to create a single non-cycling workflow of repeating tasks, each
   with its own individual *cycle point*.

.. image:: ../img/cycling.png
   :align: center

This removes the artificial barrier between cycles. Cylc tasks can advance
constrained only by their individual dependencies, for maximum concurrency
across as well as within cycles. This allows fast catch-up from delays in
real time systems, and sustained high throughput off the clock.


How to Run User Guide Examples
------------------------------

Many Cylc concepts and features in this document are illustrated with minimal
snippets of workflow configuration. Most of these can be turned into a complete
workflow that you can actually run, with a few easy steps:

- Add scheduling section headings, if missing, above the graph
- Use ``allow implicit tasks = True`` to automatically create dummy definitions
  for each task
- Configure the ``root`` task family to make the dummy jobs take a little time
  to run, so the workflow doesn't evolve too quickly
- For cycling graphs, configure an initial cycle point to start at

For example, here is a small cycling workflow graph:

.. code-block:: cylc-graph

   # Avoid caffeine withdrawal
   PT6H = "grind_beans => make_coffee => drink_coffee"

And here it is as a complete runnable workflow:

.. code-block:: cylc

   [scheduler]
       allow implicit tasks = True
   [scheduling]
       initial cycle point = now
       [[graph]]
           # Avoid caffeine withdrawal
           PT6H = "grind_beans => make_coffee => drink_coffee"
   [runtime]
       [[root]]
           script = "sleep 10"
