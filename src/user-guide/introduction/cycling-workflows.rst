Cylc and Cycling Workflows
==========================

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

.. image:: ../../img/cycling.png
   :align: center

This removes the artificial barrier between cycles. Cylc tasks can advance
constrained only by their individual dependencies, for maximum concurrency
across as well as within cycles. This allows fast catch-up from delays in
real time systems, and sustained high throughput off the clock.
