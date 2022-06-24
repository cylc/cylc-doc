.. _728.remote_owner:

Remote Usernames
================

.. admonition:: does this change affect me?
   :class: tip

   * If you set :cylc:conf:`flow.cylc[runtime][<namespace>][remote]owner`
   * If you use ``--owner`` on the command line


Overview
--------

If your username differs beteen the :term:`scheduler` host and job hosts, then
you may have configured Cylc to run jobs under the correct account using
:cylc:conf:`flow.cylc[runtime][<namespace>][remote]owner`
or used the ``--owner`` Cylc command line option
with commands which access remote hosts.

.. _SSH configuration file: https://man.openbsd.org/ssh_config

Cylc no longer supports specifying the username in this way, we suggest
configuring your remote username using the `SSH configuration file`_ e.g:

.. code-block:: none

   Host MyHost
     User root

SSH will then automatically use the configured username when connecting to the
remote machine.

Since Cylc uses SSH and RSync to manage job hosts, the SSH config also configures
Cylc.

.. note::

   This approach using the SSH configuration file also works with Cylc 7.
