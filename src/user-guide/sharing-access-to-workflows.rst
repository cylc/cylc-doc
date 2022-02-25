.. _Authorization:

Authorizing Others to Access Your Workflows
===========================================

The Cylc UI Server supports multi user access. You can grant control of your
workflows to other users, by adding or removing privileges on a Cylc operation
basis. This requires site level configuration, with individual users being able
to set authorization settings, within the bounds set by the site.

Sites can set default access rights for users, for more information, see
:ref:`site_configuration`.

Note, if this feature is not configured, the default is no multi user access,
only the workflow owner will be able to interact with it.

If you grant access to another user, this access will apply to all of your
workflows.

Granting Access
---------------

There are three methods of identifying a user to grant access to:

- ``*`` character, to indicate any authenticated user,
- using the ``group:`` prefix to indicate a system group. E.g.
  ``group:groupname``, will assign permissions to all members of the system
  group named ``groupname``. For more information, see :ref:`group_support`.
- ``username`` to indicate a specific user.


Using glob (``*``) to pattern match usernames and group names is not currently
supported.

Permissions are additive. If the user appears elsewhere in configuration, for
example as a member of a system group, the permission level is taken as the
greatest possible.

However, negations take precedence.

Note, defaults in site config only apply if a user does not appear in the
``c.CylcUIServer.user_authorization``.

Methods of Assigning Permissions
--------------------------------
Assigning permissions can be done in two ways:

 - using individual Cylc operations, e.g. ``play``, ``pause``
 - using predefined access groups: ``READ``, ``CONTROL``, ``ALL``.

Using both methods is supported, e.g ["READ", "stop", "pause"]

Individual Operations
^^^^^^^^^^^^^^^^^^^^^
To assign users permissions, you can list the operations you wish to grant

.. code-block:: python

   c.CylcUIServer.user_authorization = {
       "user1": ["read", "pause", "play"]
   }

Provided you have permission (via the site config file) to grant ``user1``
these permissions, this will result in ``user1`` being able to see your
workflows (from the ``read`` operation), and ``pause`` and ``play`` your workflows.


To remove permissions prepend the operation with a ``!``.
For example,

.. code-block:: python

   c.CylcUIServer.user_authorization = {
       "group:groupA": ["read", "play", "stop"],
       "user2": ["!stop"]
   }

Providing your site configuration permits you to grant this access,
this configuration, for ``user2`` (who is a member of system group ``groupA``),
would result in them having ``read`` and ``play`` access. Permission to stop your
workflows has been removed so this action will be forbidden.

Access Groups
^^^^^^^^^^^^^
For convenience, cylc operations available in the UI have been bundled into
access groups. These should be capitalized to distinguish from cylc operations.

We currently support ``READ``, ``CONTROL`` and ``ALL`` and to remove permissions
to operations in these groups, use ``!READ``, ``!CONTROL``, ``!ALL``.


.. csv-table:: Access Group Mappings
   :header: "Operation", "READ", "CONTROL", "ALL"

   "Broadcast", , , "X"
   "Ext-trigger",, "X", "X"
   "Hold",, "X", "X"
   "Kill",, "X", "X"
   "Message",, "X", "X"
   "Pause",, "X", "X"
   "Play",, "X", "X"
   "Poll",, "X", "X"
   "Read","X", , "X"
   "Release",, "X", "X"
   "ReleaseHoldPoint",, "X", "X"
   "Reload",, "X", "X"
   "Remove",, "X", "X"
   "Resume",, "X", "X"
   "SetGraphWindowExtent",, "X", "X"
   "SetHoldPoint",, "X", "X"
   "SetOutputs",, "X", "X"
   "SetVerbosity",, "X", "X"
   "Stop",, "X", "X"
   "Trigger",, "X", "X"


.. note::

   The ``READ`` access group is shorthand for all read-only operations. At present,
   this is solely the ``read`` operation, which grants access to GraphQL queries and
   subscriptions, and enables users to see the workflows in the UI. In future
   the ``READ`` access group may be extended.

.. note::

   Granting CONTROL access does not automatically grant READ access.

.. _user_configuration:

User Authorization Configuration
--------------------------------
``c.CylcUIServer.user_authorization``, which is loaded from
``~/.cylc/hub/jupyter_config.py``, contains your preferences for granting access
to other users. This configuration should be entered as a Python
dictionary. If a user does not appear in your user config, the default site
access will apply.
You are only permitted to grant access, within the bounds set at site level.

Example User Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^

An example user configuration:

.. code-block:: python

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

Site Authorization Configuration
--------------------------------
The site_authorization configuration allows sites to configure sensible defaults
and limits for the permissions users can delegate.

Note that as the UI Server runs as the workflow owner, they have full control
over it and in theory may bypass these restrictions in a variety of ways. As an
extreme example, a workflow owner could pass their account credentials to
another person, and that cannot be prevented by technical means. However, a
workflow owner cannot unilaterally gain access to any other user's account or
workflows by configuring their own UI Server.

``c.CylcUIServer.site-authorization``, which is loaded from
``/etc/cylc/hub/jupyter_config.py``, or, alternatively, the environment variable
``CYLC_SITE_CONF_PATH``, contains these site default and limit settings for
users. This configuration should be entered as a Python dictionary.


Defaults and Limits
^^^^^^^^^^^^^^^^^^^
Sites set both limits and defaults for users.

- ``limit`` determines the maximum access users can grant to their workflows.

- ``default`` sets a default access level, which applies if the user does
  not appear in the user-authorization configuration (via explicit user name or group).

Missing Configurations in Site Authorization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For site configuration:

* if a limit is not set but a default is, then the limit is the default.
* if a default is not set but a limit is, then the default is no access.


Example Site Authorization Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Whilst most site configurations will be simpler than the example below, this
example provides an indication of the combinations available.

.. code-block:: python

   c.CylcUIServer.site_authorization = {
       "*": {  # For all ui-server owners,
           "*": {  # Any authenticated user
               "default": "READ",  # Will have default read-only access
           },
           "user1": {  # for all ui-server owners, user1
               "default": ["!ALL"],  # has no privilidges by default
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


.. _group_support:

Group Support
^^^^^^^^^^^^^
Unix-like systems support grouping users. Cylc authorization supports granting
access by membership of these system groups. You can indicate a system group
by using the ``group:`` indicator.

System groups are found by
  :py:mod:`get_groups<cylc.uiserver.authorise.get_groups>`

  .. autofunction:: cylc.uiserver.authorise.get_groups


Changing Access Rights
^^^^^^^^^^^^^^^^^^^^^^
Changing authorization permissions in your ``jupyter_config.py`` will require the
UI Server to be restarted before any changes are applied.

Interacting with Others' Workflows
----------------------------------

The authorization system in Cylc 8 is complete, although expect access to other
users' workflows via the UI to be further developed in future.

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

- the server has been started by the user of the workflows you are trying to
  access. Users currently can only spawn their own UI Servers.
