Expire Triggers
=========================

* When the condition is met, the task will generate the ``expired`` output rather than just being removed.
* The ``expired`` output will be marked as :term:`optional <optional output>` for the triggered task, but a custom `flow.cylc[runtime][<namespace>]completion` condition will need to be modified accordingly.
* This should be functionally equivalent to "suicide triggers" in that the triggered task will not run.
* However, the triggered task will now be left in the ``expired`` state making it clearer in the GUI/logs that the task has been triggered in this way.
* It is possible to trigger other tasks off of this ``expired`` output for more advanced failure recovery.
