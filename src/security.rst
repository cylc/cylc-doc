Security
========

TODO: Fill in other parts of this document, with information about
cylc-flow (jobs, zmq, etc), UI Server, etc.

Web
---

TODO: write some introduction about web security in Cylc 8,
UI Server, OAuth, JupyterHub Authenticators, etc.

WebSockets
^^^^^^^^^^

Frontend and backend communication with WebSockets in Cylc is secured through
WebSocket Secure, cookie-based authentication, and same origin backend
verification.

WebSocket Secure
""""""""""""""""

The WebSocket protocol supports the ``ws`` and the ``wss`` protocol URI
identifiers. The former means "WebSocket", and the latter means
"WebSocket Secure". It is recommended to use ``wss`` so that the
communication is encrypted and attacks such as MITM are avoided.

The ``wss`` identifier can only be used when SSL is enabled. JupyterHub
has `a section on how to enable SSL`_ in their documentation. Once SSL
is enabled the Cylc web UI automatically detects it and uses ``wss``.

.. _`a section on how to enable SSL`: https://jupyterhub.readthedocs.io/en/stable/getting-started/security-basics.html#enabling-ssl-encryption

Cookie-based authentication
"""""""""""""""""""""""""""

When the frontend initiates the communication with the backend it will send
an HTTP request that will include the client cookies. The backend expects
a valid `JupyterHub user cookie`_.

.. _`JupyterHub user cookie`: https://jupyterhub.readthedocs.io/en/latest/getting-started/security-basics.html#jupyterhub-user-username

If the cookie is valid a connection will be established and
the query response will be sent to the frontend.

If the cookie is invalid (e.g. cookie secret changed in the server)
or if the cookie is not present (e.g. user not authenticated)
the backend will return an HTTP 403 error and the connection
will be closed.

If the backend log level is set to ``DEBUG`` a message will be
emitted in the logs alerting about the unauthorized access.

Same-origin verification
""""""""""""""""""""""""

When a client tries to open a WebSocket with the Cylc UI Server, it
will pass by a same-origin verification. This test is useful to prevent
attacks such as `CORS`_.

This verification only occurs when the client provides an ``Origin``
HTTP header - which browsers normally do. Command line applications
do not necessarily provide this header, but CORS is normally not an
issue for that case.

Cylc UI Server uses Tornado's default `same-origin policy`_.
So whenever a client sends a request with the ``Origin`` header,
the server will compare it against the ``Host`` HTTP header.

If these values do not match, an error is logged and returned to the
client.

.. _`CORS`: https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny
.. _`same-origin policy`: https://www.tornadoweb.org/en/stable/websocket.html#tornado.websocket.WebSocketHandler.check_origin
