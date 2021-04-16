Workflow Runtime Interface
=======================

Cylc suites are TCP servers which use the ZeroMQ protocol to communicate with
clients and jobs.

Cylc provides a Python client to communicate with this server
:py:class:`cylc.flow.network.client.WorkflowRuntimeClient`

.. code-block:: python

   >>> from cylc.flow.network.client import WorkflowRuntimeClient
   >>> client = WorkflowRuntimeClient('my-suite')
   >>> client('ping_suite')
   True

Cylc also provides sub-command called ``cylc client`` which is a simple
wrapper of the Python client.

.. code-block:: console

   $ cylc client generic ping_suite -n
   true

The available "commands" or ("endpoints") are contained in
:py:class:`cylc.flow.network.server.WorkflowRuntimeServer` class.


Client
------

.. autoclass:: cylc.flow.network.client.WorkflowRuntimeClient


Server
------

.. autoclass:: cylc.flow.network.server.WorkflowRuntimeServer
   :members:
