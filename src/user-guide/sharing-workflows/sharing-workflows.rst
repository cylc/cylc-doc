.. _Authorization:

Authorization
=============

Cylc supports multi user access. You can grant control of your
workflows to other users, by adding or removing privileges on a Cylc operation
basis.This requires site level configuration, with individual users being able
to set authorization settings, within the bounds set by the site.

Sites can set default access rights for users, for more information, see
:ref:`site_configuration`.

Note, if this feature is not configured, the default is no multi user access
and access will be limited to the workflow owner.

If you grant access to another user, this access will apply to all workflows.

Granting Access
---------------

There are three methods of identifying a user to grant access to:

- ``*`` character, to indicate any authenticated user,
- using the ``group:`` prefix to indicate a system group. E.g.
  ``group:groupname``, will assign permissions to all members of the system
  group named `groupname`. For more information, see :ref:`group_support`.
- ``username`` to indicate a specific user.

All permissions are additive, if user appears elsewhere in configuration, for
example as a member of a system group, the permission level is taken as the
greatest possible.

However, any negations are applied with priority.

Note, default in site config does not contribute to permissions, this is used
in the case where a user does not appear in the `c.CylcUIServer.user-authorization`.

.. note::

   Spellings of UIServer configurations should be strictly adhered to. Using,
   for example, `c.CylcUIServer.user-authorisation` rather than
   `c.CylcUIServer.user-authorization` would result in cylc silently ignoring
   this configuration.

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

Provided you have permission to give `user1` these permissions, as defined in the
site configuration file, this will result in `user1` being able to see your
workflows (from the `read` operation), and `pause` and `play` your workflows.


Removing permissions can be achieved by prepending the operation with a ``!``.
For example,

.. code-block:: python

   c.CylcUIServer.user_authorization = {
       "group:groupA": ["read", "play", "stop"],
       "user2": ["!stop"]
   }

Again, providing your site configuration permits you to grant this access,
this configuration, for `user2` (who is a member of system group `groupA`) would
result in them having "read" and "play" access. The the access to stop your workflows
has been removed and this action will be forbidden.

Access Groups
^^^^^^^^^^^^^
For convenience, cylc operations available in the ui have been bundled into
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
   "Ping","X", , "X"
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

   ``READ`` access group (which exands to ``["read", "ping"]``) is a method for
   granting non-interactive access.

.. _user_configuration:

User Authorization Configuration
--------------------------------
`c.CylcUIServer.user-authorization`, which is loaded from
`~/.cylc/hub/jupyter_config.py`, contains your preferences for granting access
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
  workflows and ping them on the gui.

- ``"group:groupA"`` applies ``CONTROL`` permissions to any member of system
  `groupA`.
  Note that, since permissions are additive, these users will gain ``READ`` access
  from the ``"*":["READ"]`` assignment.

- ``"user1"`` will have permission to view workflows, ``pause`` but not ``play``
  workflows, even if `user1` is a member of the system `groupA`. This is due to
  negations taking precedence over additions.

- ``"user2"`` is not permitted to view workflows, or perform any operations. 

.. _site_configuration:

Site Authorization Configuration
--------------------------------
`c.CylcUIServer.site-authorization`, which is loaded from
`/etc/cylc/hub/jupyter_config.py`, or, alternatively, the environment variable
``CYLC_SITE_CONF_PATH``, contains default and limit settings for users. This
is set at a site level. This configuration should be entered as a Python
dictionary.


Defaults and Limits
^^^^^^^^^^^^^^^^^^^
Sites set both limits and defaults for users.

- `limit` will determine if a user has the privileges to give away access to 
  their workflows. 

- `default` sets a default access level, which is activated if the user does
  not appear in the user-authorization configuration.


Missing Configurations in Site Authorization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Site configuration 

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

.. TODO - link to method getgroups() in uiserver, once Auth PR merged. 

Changing Access Rights
^^^^^^^^^^^^^^^^^^^^^^
Changing authorization permissions in your `jupyter_config.py` will require the
UI Server to be restarted before any changes are applied.

Interacting with Others Workflows
---------------------------------
If you have been granted access to another users workflows, you can view and
interact with these workflows.
Say, you, userA, wishes to interact with userB's workflows.
You can do this by changing the URL `https://<hub>/user/userB`, using the hub
of the userB. You should authenticate as yourself (userA) and, provided you
have the correct permissions, you will see userB's workflows for interaction.


Troubleshooting Authorization
-----------------------------

If authorization is not performing as expected, check

- you are permitted to give away access in the site configuration.

- you have provided `read` permissions, this enables the user to see your
  workflows.

- check the spelling in your configuration. The correct spelling is 
  `c.CylcUIServer.user_authorization`
