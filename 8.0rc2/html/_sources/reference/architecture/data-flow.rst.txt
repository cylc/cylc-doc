Data Flow
=========

This section looks at how Cylc synchronises data between its different
components, the transports, security and formats used to do so.

.. digraph:: _
   :align: center

   Jobs -> Scheduler [label=" ZMQ\n GraphQL\n (default)"]

   Scheduler -> UIS [label=" ZMQ\n GraphQL (control)\n Protobuf (data)"]

   UIS -> UI [label=" Websocket\n GraphQL"]


.. _arch protocols:

Protocols, Transport & Security
-------------------------------

Cylc uses the following schemes for data and control:


.. _arch zmq:

ZMQ (Over TCP)
^^^^^^^^^^^^^^

Cylc uses `ZMQ`_ over TCP for most server side interaction.

All `ZMQ`_ connections are secured by `CurveZMQ`_ which uses security keys
which are stored on the filesystem with appropriate permissions.

Where remote communication is involved Cylc synchronises the relevant keys
to the appropriate platforms.

For more information on the key files see :ref:`Authentication Files`.

.. _arch ssh:

SSH
^^^

SSH connections are used for some purposes such as installing the key files
required for :ref:`arch zmq` transport.

.. _arch https:

HTTPS (Hypertext Transfer Protocol Secure)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

HTTPS connections are used in the browser-based `Cylc UI`_. The certificate
used must be configured with the `Cylc UI Server`_ / `Jupyter Server`_.

.. _arch wss:

WSS (WebSocket Secure)
^^^^^^^^^^^^^^^^^^^^^^
Websocket connections are used in the browser-based `Cylc UI`_. These
connections are upgraded from HTTPS connections and share the same security.

.. _arch formats:

Formats
-------

Cylc uses the following transports to communicate over these protocols.

.. _arch protobuf:

Protobuf
^^^^^^^^

Protobuf is both a storage utility and transport.

Protobuf is used for internal data stores and the synchronisation of those data
stores.


.. _arch graphql:

GraphQL
^^^^^^^

`GraphQL`_ is a query language which is intended to be the user-facing
data and control interface for Cylc workflows.

It contains both data and mutations (actions) defined by a self-documenting
schema.

The GraphQL servers get their data from :ref:`arch protobuf` data stores.


Component Interactions
----------------------

Here are some additional details on how the components interact.

Job -> Scheduler
^^^^^^^^^^^^^^^^

:Default :Protocol: :ref:`arch zmq`
:Format: :ref:`arch graphql`

Jobs can communicate status updates back to the Scheduler using different
methods. The method used is configured on a per-platform basis by the
:cylc:conf:`global.cylc[platforms][<platform name>]communication method`.


Client -> Scheduler
^^^^^^^^^^^^^^^^^^^

:Protocol: :ref:`arch zmq`
:Format: :ref:`arch protobuf`

The subcommands in the Cylc command line interface map onto `GraphQL`_
mutations.

Mutations are issued through `ZMQ`_ connections.

Scheduler -> UI Server
^^^^^^^^^^^^^^^^^^^^^^

:Protocol: :ref:`arch zmq`
:Formats: :ref:`arch protobuf` (data) and :ref:`arch graphql` (control)

The :term:`Scheduler` maintains an in-memory `Protobuf`_ data store which is
backed up by a SQLite3 database.

The database provides crash resilience and restart capability.

The `UI Server`_ also maintains an in-memory `Protobuf`_ data store containing
relevant data for the workflows it is actively monitoring.

The synchronisation of the :term:`Scheduler` and `UI Server`_ data stores is
done using one :ref:`arch zmq` connection per :term:`Scheduler`.

The :term:`Schedulers <scheduler>` that the `UI Server`_ connects to are
determined by the active subscriptions registered. If there are no active
subscriptions the `UI Server`_ will have no active :term:`Scheduler`
connections.


UI Server -> UI
^^^^^^^^^^^^^^^

:Protocols: :ref:`arch wss`, :ref:`arch https`
:Format: :ref:`arch graphql`

Most UI functionality involves subscribing to "delta" updates. For these
subscriptions the `UI Server`_ sends only the added/removed/updated data
(a delta) to the UI enabling it to update its internal data store.

The UI maintains a flat "lookup" which contains all objects in the store
indexed by their ID. It also maintains a "tree" which contains references
to the data in the "lookup" (but does not duplicate it) which it holds in a
hierarchical structure more suitable for presentation purposes.

The Cylc Web UI uses `Apollo Client`_ to handle `GraphQL`_ requests.
It will have one `WebSocket`_ per user session.

.. figure:: img/websocket-communication.png
   :align: center

Every message received by the server is added to a queue, and processed
by the server as soon as possible.

It uses the Cylc UI Server schema and resolvers to validate the
query and to fetch data from the data store for the query response.

The query result is then serialized as JSON and sent back to the client.
The work of the Apollo Client ends after it pushes the data to the Vuex
store.

The communication between client and server follows a protocol
called `graphql-ws protocol`_.

.. figure:: img/websocket-graphql-ws-protocol.png
   :align: center

After a channel between client and server is open, the messages
follow that protocol, starting by the ``connection init`` message,
that simply expects an ``ack`` message back from the server,
where the ``ack`` is an acknowledgement to the client - note
that the protocol does not define an ``ack`` as a MUST, but
rather as a MAY, so a client may interpret not receiving an
error as an acknowledgement to proceed as well.

The next message will be a ``start``, which will contain the
GraphQL query subscription. If there were no errors, the client and
server subscription is established, and the client will start
receiving the GraphQL responses.

The protocol also supports other messages, such as ``stop``, to
tell the server it doesn't need to send any more data as that
subscription is now cancelled.


.. _`GraphQL subscription`: https://www.apollographql.com/docs/react/data/subscriptions/
.. _`graphql-ws protocol`: https://github.com/apollographql/subscriptions-transport-ws/blob/master/PROTOCOL.md
