.. _cylc.uiserver.multi-user:

Authorizing Others to Access Your Workflows
===========================================

For multi-user setups, the Cylc web GUI can be deployed as part of a
`Jupyter Hub`_ setup where a central service spawns servers on behalf of users.

The Cylc UI Server can be configured to allow specified users to monitor and
optionally control workflows running under other user accounts.

This has many use cases including:

* Collaborative research setups where multiple users need to access the same
  workflow.
* Production systems where different levels of support may have different
  levels of access.
* Support where administrators may require access to users workflows.

A multi-user Cylc setup consists of three components:

1. `Jupyter Hub`_
2. `Jupyter Server`_
3. `Cylc UI Server`_

And may additionally include other Jupyter Server extensions such as
`Jupyter Lab`_ to provide a full interactive virtual workstation in the
browser.

In order to allow access to other users servers, to permit the monitoring and
optionally control of other users workflows, each of these three components
must be configured:

1. `Jupyter Hub`_ must be configured to allow connections to other users servers.
2. The `Jupyter Server`_ authorisation policy must be set.
3. Cylc must be configured with user permissions.

This configuration can all be performed in the same Jupyter / Cylc UI Server
configuration file see :ref:`UI_Server_config` for more details.

.. rubric:: Quick Example:

.. code-block:: python

   # /etc/cylc/uiserver/jupyter_config.py

   # 1. Jupyter Hub
   #    Allow all authenticated users to access, start and stop
   #    eachothers servers
   c.JupyterHub.load_roles = [
       {
           "name": "user",
           "scopes": ["self", "access:servers", "servers"],
       }
   ]


   # 2. Jupyter Server
   #    Set a safe authorisation policy for multi-user setups
   #    Note: This is ONLY necessary if you are deploying the Cylc UI Server
   #          using commands other than `cylc hub` and `cylc hubapp`,
   #          otherwise, it is the default.
   from cylc.uiserver.authorise import CylcAuthorizer
   c.ServerApp.authorizer_class = CylcAuthorizer


   # 3. Cylc
   #    Delegate permissions to users
   c.CylcUIServer.user_authorization = {
       # proivide all authenticated users with read-only access to eachothers
       # servers
       "*": ["READ"],
   }

The rest of this document takes you through each of these configurations, some
of the key options and how they relate to their respective systems.


.. _jupyterhub.authorization:

Jupyter Hub Authorisation
-------------------------

By default, `Jupyter Hub`_ only allows users to access their own servers.

In order to allow access to other users servers, two scopes must be configured:

``access:servers``
   Permits us to connect to another users server.
``servers``
   Permits us to start another users server.

This is done using the
:py:attr:`c.JupyterHub.load_roles <jupyterhub.app.JupyterHub.load_roles>`
configuration.
For more information see the
:ref:`JupyterHub scopes reference <jupyterhub-scopes>`.

Example:

.. code-block:: python

   # /etc/cylc/uiserver/jupyter_config.py

   c.JupyterHub.load_roles = [
       {
           # allow all authenticated users to access, start and stop
           # eachother's servers
           "name": "user",
           "scopes": ["self", "access:servers", "servers"],
       }
   ]


.. _jupyterserver.authorization:

Jupyter Server Authorisation
----------------------------

.. tip::

   You can skip this section if you are starting Jupyter Hub using ``cylc hub``
   command and have not overridden the
   :py:attr:`c.JupyterHub.spawner_class <jupyterhub.app.JupyterHub.spawner_class>`
   configuration (so are spawning the ``cylc hubapp`` command).

.. autoclass:: cylc.uiserver.authorise.CylcAuthorizer


.. _cylc.uiserver.user_authorization:

Cylc User Authorisation
-----------------------

Cylc Authorisation is configurable on a per-user and per-command basis but
not on a per-workflow basis.

By default users can only see and interact with their own workflows.

Sites can restrict the permissions which users are allowed to delegate to each
other and can configure default permissions (see :ref:`site_configuration`).

Authorization is configured by these two configurations:

* :py:attr:`c.CylcUIServer.user_authorization
  <cylc.uiserver.app.CylcUIServer.user_authorization>` (user configuration)
* :py:attr:`c.CylcUIServer.site_authorization
  <cylc.uiserver.app.CylcUIServer.site_authorization>` (site configuration)

.. rubric:: Example:

.. code-block:: python

   # ~/.cylc/uiserver/jupyter_config.py

   c.CylcUIServer.user_authorization = {
       # <user/group>: [<permission>, ...],

       # allow "user1" to monitor my workflows
       "user1": ["READ"],

       # allow "user2" to monitor and trigger tasks in my workflows
       "user2": ["READ", "Trigger"],
   }


Users
^^^^^

There are three methods of identifying a user to grant access to:

``<username>``
  Configures permissions for a singe user.
``group:<groupname>``
  Configures a user group. For more information, see :ref:`group_support`.
``*``
  Configures permissions for any authenticated user (see
  :ref:`Jupyter Hub authenticators reference <authenticators-reference>`
  for details).

.. note::

   Using glob patterns (e.g. ``*``) to pattern match user and group names is
   not currently supported.


Permissions
^^^^^^^^^^^

.. TODO: autogenerate this permission list
   https://github.com/cylc/cylc-uiserver/issues/466

Permissions can be granted for each Cylc command individually, for convenience
commands are arranged into groups to avoid having to list them individually:

``READ`` (i.e. read-only access)
  A user with read permissions may view workflows, monitor tasks states and
  open log files, but they cannot interact with the workflows.

  * ``Read``
``CONTROL`` (e.g. start & stop workflows)
  A user with control permissions may issue commands to interact with workflows
  and can start/stop workflows but cannot redefine the workflow configuration
  itself (without direct filesystem access).

  * ``Clean``
  * ``Ext-trigger``
  * ``Hold``
  * ``Kill``
  * ``Message``
  * ``Pause``
  * ``Play``
  * ``Poll``
  * ``Release``
  * ``ReleaseHoldPoint``
  * ``Reload``
  * ``Remove``
  * ``Resume``
  * ``SetGraphWindowExtent``
  * ``SetHoldPoint``
  * ``SetOutputs``
  * ``SetVerbosity``
  * ``Stop``
  * ``Trigger``
``ALL`` (i.e. full control)
  A user with all permissions may alter task configuration so may inject
  arbitrary code into the workflow.

  * ``Broadcast``

.. note::

   With the exception of ``Read`` all of the above permissions map onto the
   Cylc GraphQL mutations which themselves map onto the command line.

   E.G. the ``Play`` permission maps onto ``mutation play`` in the GraphQL
   schema and ``cylc play`` on the command line.

   To find out more about a command, see the GraphQL or CLI documentation.

By default, users have ``ALL`` permissions for their own workflows and no
permissions to other users workflows.

Permissions are additive, so delegating both ``READ`` and ``CONTROL`` would
provide all permission in both groups.

The ``!`` character can be used to subtract permissions, e.g. delegating
``CONTROL`` and ``!Stop`` would provide all control permissions except stop.

.. note::

   Granting acess to a group does not automatically grant access to lower
   groups e.g. granting ``CONTROL`` access does not automatically grant
   ``READ`` access.


Examples
^^^^^^^^

.. code-block:: python

   # ~/.cylc/uiserver/jupyter_config.py

   c.CylcUIServer.user_authorization = {
       "*": ["READ"],
       "group:groupA": ["CONTROL"],
       "user1": ["read", "pause", "!play"],
       "user2": ["!ALL"]
   }

In this scenario:

- ``"*"``  represents any authenticated user. They have permission to view all
  workflows, and view them on the GUI.
- ``"group:groupA"`` applies ``CONTROL`` permissions to any member of system
  ``groupA``.
  Note that, since permissions are additive, these users will gain ``READ`` access
  from the ``"*":["READ"]`` assignment.
- ``"user1"`` will have permission to view workflows, ``pause`` but not ``play``
  workflows, even if ``user1`` is a member of the system ``groupA``. This is due
  to negations taking precedence over additions.
- ``"user2"`` is not permitted to view workflows, or perform any operations.


.. _site_configuration:

Cylc Site Configuration
-----------------------

The :py:attr:`c.CylcUIServer.site authorization
<cylc.uiserver.app.CylcUIServer.site_authorization>` configuration allows sites
to configure sensible defaults and limits for the permissions users can
delegate.

It takes the form:

.. code-block:: python

   {
     "<owner>": {
       "<user>": {
         "default": [],
         "limit", []
       }
     }
   }

Where ``<owner>`` is the username of the account that is running a server and
``<user>`` is the username of an account trying to connect to it.

Sites can set both limits and defaults for users:

``limit``
   Determines the maximum access users can grant to their workflows.
``default``
   Sets a default access level, which applies if the user does not appear in
   the user_authorization configuration (via explicit user name or group).

   Note, these defaults apply only if a user does not appear in
   :py:attr:`c.CylcUIServer.user_authorization
   <cylc.uiserver.app.CylcUIServer.user_authorization>`.

* If a limit is not set but a default is, then the limit is the default.
* If a default is not set but a limit is, then the default is no access.

.. note::

   As the UI Server runs as the workflow owner, the owner has full control over
   it and in theory may bypass these restrictions in a variety of ways. As an
   extreme example, a workflow owner could pass their account credentials to
   another person. This cannot be prevented by technical means. However, a
   workflow owner cannot unilaterally gain access to any other user's account
   or workflows by configuring their own UI Server.

.. note::

   Changes to the Cylc authorization configuration will take effect when the
   Cylc UI Server is restarted.


.. _group_support:

Group Support
^^^^^^^^^^^^^

Unix-like systems support user groups. Cylc authorization supports granting
access by membership of these system groups. You can indicate a system group
by using the ``group:`` indicator.

System groups are found by
:py:mod:`get_groups<cylc.uiserver.authorise.get_groups>`

.. autofunction:: cylc.uiserver.authorise.get_groups


Example Site Authorization Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Whilst most site configurations will be simpler than the example below, this
example provides an indication of the combinations available.

.. code-block:: python

   # /etc/cylc/uiserver/jupyter_config.py

   c.CylcUIServer.site_authorization = {
       "*": {  # For all ui-server owners,
           "*": {  # Any authenticated user
               "default": "READ",  # Will have default read-only access
           },
           "user1": {  # for all ui-server owners, user1
               "default": ["!ALL"],  # has no privileges by default
           },  # No limit set, so all ui-server owners are unable to permit user1
       },
       "server_owner_1": {  # For specific UI Server owner, server_owner_1
           "*": {  # Any authenticated user
               "default": "READ",  # Will have default read-only access
               "limit": ["READ", "CONTROL"],  # server_owner_1 is able to give away
           },  # READ and CONTROL privileges.
       },
       "server_owner_2": {  # For specific UI Server owner,
           "user2": {  # Specific user2
               "limit": "ALL"  # Can only be granted a maximum of ALL by
           },  # server_owner2, default access for user2 falls back to
           # standard READ only (if server_owner_2/user2 are
           # included in other auth config e.g. the top example),
           # or none if not in any other auth config sections.
           "group:groupA": {  # group denoted with a `group:`
               "default": [
                   "READ",
                   "CONTROL",
               ]  # groupA has default READ, CONTROL access to server_owner_2's
           },  # workflows
       },
       "group:grp_of_svr_owners": {  # Group of users who own UI Servers
           "group:groupB": {
               "default": "READ",  # can grant groupB users up to READ and CONTROL
               "limit": [  # privileges, without stop and kill
                   "READ",
                   "CONTROL",
                   "!stop",  # operations
                   "!kill",
               ],
           },
       },
   }


Interacting with Others' Workflows
----------------------------------

.. spelling:word-list::

   userA
   userB

If you have been granted access to another user's workflows, you can view and
interact with these workflows.
Say, you, userA, wish to interact with userB's workflows.
You can do this by navigating to the URL ``https://<hub>/user/userB``, using
the hub of userB. You should authenticate as yourself (userA) and, provided you
have the correct permissions, you will see userB's workflows for interaction.

.. note::

   Operations that are not authorized will appear greyed out on the UI.


Troubleshooting Authorization
-----------------------------

If authorization is not performing as expected, check

- you are permitted by the site configuration to give away access.
- you have provided ``read`` permissions, which enables the user to see your
  workflows.
- check the spelling in your configuration. The correct spelling is
  ``c.CylcUIServer.user_authorization``
