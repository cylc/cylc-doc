.. _SiteAndUserConfiguration:

Global (Site, User) Configuration Files
=======================================

Cylc site and user global configuration files contain settings that affect all
suites. Some of these, such as the range of network ports used by cylc,
should be set in the site ``flow.rc`` config file. Legal items,
values, and system defaults are documented in :ref:`SiteRCReference`.

Others, such as the preferred text editor for suite configurations,
can be overridden by users in ``~/.cylc/flow/<CYLC_VERSION>/flow.rc``.


How to create a site or user flow.rc config file
------------------------------------------------

The ``cylc get-global-config`` command prints global config defaults,
overridden by site global settings (if any), overridden by user global
settings (if any).

To generate a new global config file:

1. Run ``$ cylc get-global-config > flow.rc``
2. Edit any settings that you need to modify.
3. Delete or comment out any seeting you do not need (to avoid inadvertently
   overriding defaults or site settings that may change in the future).

For all legal items, see the :ref:`SiteRCReference`.


File locations:
^^^^^^^^^^^^^^^

- **Site**: ``/etc/cylc/flow/<CYLC_VERSION>/flow.rc``
- **User**: ``$HOME/.cylc/flow/<CYLC_VERSION>/flow.rc``
