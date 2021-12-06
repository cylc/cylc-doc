.. |task-waiting| image:: ../../img/task-job-icons/task-waiting.png
   :scale: 100%
   :align: middle

.. |task-expired| image:: ../../img/task-job-icons/task-expired.png
   :scale: 100%
   :align: middle

.. |task-preparing| image:: ../../img/task-job-icons/task-preparing.png
   :scale: 100%
   :align: middle

.. |task-submitted| image:: ../../img/task-job-icons/task-submitted.png
   :scale: 100%
   :align: middle

.. |task-submit-failed| image:: ../../img/task-job-icons/task-submit-failed.png
   :scale: 100%
   :align: middle

.. |task-running| image:: ../../img/task-job-icons/task-running.png
   :scale: 100%
   :align: middle

.. |task-succeeded| image:: ../../img/task-job-icons/task-succeeded.png
   :scale: 100%
   :align: middle

.. |task-failed| image:: ../../img/task-job-icons/task-failed.png
   :scale: 100%
   :align: middle


.. |job-blank| image:: ../../img/task-job-icons/job-blank.png
   :scale: 100%
   :align: middle

.. |job-submitted| image:: ../../img/task-job-icons/job-submitted.png
   :scale: 100%
   :align: middle

.. |job-submit-failed| image:: ../../img/task-job-icons/job-submit-failed.png
   :scale: 100%
   :align: middle

.. |job-running| image:: ../../img/task-job-icons/job-running.png
   :scale: 100%
   :align: middle

.. |job-succeeded| image:: ../../img/task-job-icons/job-succeeded.png
   :scale: 100%
   :align: middle

.. |job-failed| image:: ../../img/task-job-icons/job-failed.png
   :scale: 100%
   :align: middle


.. _task-job-states:

Task & Job States
=================

**Tasks** are a workflow abstraction; they represent future and past jobs as
well as current active jobs. In the Cylc UI, task states have monochromatic
icons like this: |task-running|.

**Jobs** are less abstract; they represent real job scripts submitted to run
on a :term:`job platform`, or the final status of those real jobs. In the Cylc
UI, job states have colored icons like this: |job-running|.

A single task can have multiple jobs, by automatic retry or manual triggering.


.. table::

    =======================================================     ===========
    Task & Job States                                           Description
    =======================================================     ===========
    |task-waiting|       |job-blank|          waiting           waiting on prerequisites
    |task-expired|       |job-blank|          expired           will not submit job (too far behind)
    |task-preparing|     |job-blank|          preparing         job being prepared
    |task-submitted|     |job-submitted|      submitted         job submitted
    |task-submit-failed| |job-submit-failed|  submit-failed     job submission failed
    |task-running|       |job-running|        running           job running
    |task-succeeded|     |job-succeeded|      succeeded         job succeeded
    |task-failed|        |job-failed|         failed            job failed
    =======================================================     ===========
