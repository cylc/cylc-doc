How to Run User Guide Examples
==============================

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



