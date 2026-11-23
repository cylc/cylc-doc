Expire Triggers
===============

.. admonition:: Does This Change Affect Me?
   :class: tip

   This is breaking change in the niche situation where a
   :cylc:conf:`[runtime][<namespace>]completion` expression has been
   manually specified for a suicide-triggered task -
   in which case ``or expired`` should be added to the end of the expression.


Overview
--------

Suicide triggers have been replaced by :ref:`expireTriggers`.
The ``!`` syntax will continue to work, but now tasks will be marked as
:term:`expired <expired task>` rather than just being removed from the workflow.

The ``cylc graph --show-suicide`` option has been renamed to ``cylc graph --show-expire``.
