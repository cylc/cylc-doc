.. _WorkflowStorageEtc:

Workflow Storage, Discovery, Revision Control, and Deployment
==========================================================

Cylc does not have a built-in solution for workflow storage and discovery,
revision control, and deployment, on a network.

Version control is not Cylc's core purpose, and projects may have their own
preferences and workflow meta-data requirements that are difficult to anticipate.
We can, however, recommend the use of the Rosie system which comes as a part of
*Rose* to do all of this very easily and elegantly with Cylc workflows.


.. _Rose:

Rose
----

**Rose** is *a framework for managing and running workflows of
scientific applications*, developed at the Met Office for use with
cylc. It is available under the open source GPL license.

- `Rose Documentation`_
- `Rose GitHub`_
