.. _CylcUIServer.architecture:

Cylc UI Server
==============

`Cylc Flow`_
   Provides a command line utility for monitoring and controlling
   Cylc workflows called ``cylc tui``.
`Cylc UI Server`_
   Provides a graphical utility for use in a web browser.

The `Cylc UI Server`_ connects to running workflows to provide "live" data
and accesses workflow databases and the filesystem to provide "offline" data.


Jupyter Server
--------------

The `Cylc UI Server`_ is a `Jupyter Server`_ extension like `Jupyter Lab`_.

`Jupyter Server`_ provides the web server infrastructure which is shared by
its extensions which can used to run multiple extensions simultaneously.

If desired other extensions (e.g. `Jupyter Lab`_) can be installed and
configured to run in the same server as the `Cylc UI Server`_.

See :ref:`managing-multiple-extensions` for details on managing which
extensions are run by `Jupyter Server`_.

`Jupyter Server`_ can be run in two ways, single-user (token authenticated)
and multi-user (hub authenticated).


.. _single-user mode:

Single-User Mode
----------------

In single-user mode users must start their own UI Servers from the command line.

`Jupyter Server`_ will provide them with a URL to access their server including
a secure token which provides authentication.

.. admonition:: Authentication Overview
   :class: hint

   See :ref:`server_security`:

Users can only monitor and control their own workflows.

.. image:: img/gui-arch-single-user.svg
   :width: 70%
   :align: center


Jupyter Hub
-----------

.. _Cylc Hub configuration file: https://github.com/cylc/cylc-uiserver/blob/master/cylc/uiserver/jupyter_config.py

`Jupyter Hub`_ is a multi-user server which spawns and manages a configured
service for authenticated users.

The "Cylc Hub" is a Jupyter Hub instance which is pre-configured to spawn
Cylc UI Servers, launched by the ``cylc hub`` command.
It is also possible to configure Jupyter Hub yourself, see the Cylc Hub
configuration file for more information.

Jupyter Hub supports a variety of different implementations and plugin interfaces
for:

* `Authenticating users <https://jupyterhub.readthedocs.io/en/stable/reference/authenticators.html>`_
* `Spawning user's servers <https://jupyterhub.readthedocs.io/en/stable/reference/spawners.html>`_
* `Proxying user's servers <https://jupyterhub.readthedocs.io/en/stable/reference/proxy.html>`_


.. _multi-user mode:

Multi-User Mode
----------------

Multi-user mode requires `Jupyter Hub`_ to be installed.

An administrator must start `Jupyter Hub`_ under a user account with
the required privileges to spawn UI Servers on behalf of the user.

Users then visit `Jupyter Hub`_ where they authenticate. `Jupyter Hub`_
spawns UI Servers on behalf of users and provides each with a fixed URL
(derived from the user name) using the configured proxy
(usually `Configurable HTTP Proxy`_).

Users can access each other's UI Servers providing they have been granted
permission.

*Authentication* is provided by either `Jupyter Server`_ or `Jupyter Hub`_.

*Authorization* in the `Cylc UI Server`_ is provided by Cylc. In
multi-user mode this allows users to connect to each others UI Servers for
monitoring or control purposes.

For more information on security and configuration see
:ref:`cylc.uiserver.multi-user`.

.. _Jupyter Hub technical overview: https://jupyterhub.readthedocs.io/en/stable/reference/technical-overview.html

For information on the architecture of `Jupyter Hub`_ and the
`Configurable HTTP Proxy`_ see the `Jupyter Hub technical overview`_.

.. admonition:: Authentication Overview
   :class: hint

   .. _Security In Jupyter Hub: https://jupyterhub.readthedocs.io/en/stable/reference/websecurity.html

   See `Security In Jupyter Hub`_.

.. image:: img/gui-arch-multi-user.svg
   :width: 100%
