.. _architecture.components:

Cylc 8 Components
=================

The main Cylc 8 system components are:

Cylc Scheduler
--------------

   - The workflow engine core, Python 3 based
   - Includes the **CLI** (Command Line Interface)
   - And **TUI**, a new Terminal UI application

Cylc Hub
--------

   - Authenticates users, spawns and proxies Cylc UI Servers
   - Can run as a regular or privileged user
   - (The Hub is a `Jupyterhub <https://jupyter.org/hub>`_ instance)

Cylc UI Server
--------------

   - Interacts with Schedulers and the filesystem
   - Serves the UI to users
   - Can be launched by the privileged Hub, for multi-user installations
   - Or run standalone for use by a single user
   - (The UI Server is a `Jupyter Server
     <https://jupyter-server.readthedocs.io>`_ extension)

Cylc UI
-------

   - In-browser web UI, includes:
   - A dashboard with summary information and documentation links
   - Integrated gscan (multi-workflow) side-panel
   - Responsive web design (from desktop to table to mobile)
   - Tabbed interface to display multiple workflow views
   - Command integration for interacting with task, jobs, and schedulers

Network layers
--------------

   - Incremental push updates (c.f. polled full-state updates in Cylc 7)