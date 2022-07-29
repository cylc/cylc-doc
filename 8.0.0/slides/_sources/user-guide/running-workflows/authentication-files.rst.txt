
.. _ConnectionAuthentication:

Client-Server Interaction
-------------------------

:term:`Schedulers <scheduler>` listen on dedicated network ports for
TCP communications from Cylc clients (task jobs and user-invoked commands).

Use ``cylc scan`` to see which workflows are listening on which ports on
scanned hosts.

Cylc generates public-private key pairs on the workflow server and job hosts
which are used for authentication.


.. _Authentication Files:

Authentication Files
--------------------

Cylc uses `CurveZMQ`_ to ensure that
any data, sent between the :term:`scheduler <scheduler>` and the client,
remains protected during transmission. Public keys are used to encrypt the
data, private keys for decryption.

Authentication files will be created in your
``$HOME/cylc-run/<workflow-id>/.service/`` directory at start-up. You can
expect to find one client public key per file system for remote jobs.

On the workflow host, the directory structure should contain:

.. code-block:: none

   ~/cylc-run/workflow_x
   `-- .service
       |-- client_public_keys
       |   |-- client_localhost.key
       |   `-- <any further client keys>
       |-- client.key_secret
       |-- server.key
       `-- server.key_secret

On the remote job host, the directory structure should contain:

.. code-block:: none

   ~/cylc-run/workflow_x
   `-- .service
       |-- client.key
       |-- client.key_secret
       `-- server.key

Keys are removed as soon as they are no longer required.
