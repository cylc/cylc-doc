.. _GuiLogViewer:

GUI/Web UI Log Viewer
=====================

The Cylc GUI and web UI provide a convenient log viewer for viewing workflow
and job log files directly within the interface. This section explains how to
use the log viewer to examine log files.

Viewing Log Files
-----------------

When you open a workflow or job in the GUI/web UI, you can view its log files
in the log viewer panel. The log viewer allows you to:

- View the contents of scheduler, job, and other log files
- Follow log files in real-time as they are being written
- Search through log file contents (in future versions)

Viewing Modes
-------------

The log viewer supports two viewing modes, which you can switch between using
the **HEAD/TAIL toggle button** in the log viewer toolbar:

**HEAD Mode (Default)**
   Shows the start of the log file and follows it as new lines are added.
   This is the default mode and provides the traditional experience of
   viewing log files from the beginning. Use this mode when you want to see
   the initial activity in a log file.

**TAIL Mode**
   Shows the most recent lines of the log file and follows the end as new
   lines are added. This is useful when you have a large log file and want
   to see only the latest activity without scrolling through the entire file.

Both modes support real-time following when a job or workflow is actively
logging. When you switch modes, the log viewer will scroll to show the
appropriate section of the file.

.. note::

   The mode you select is saved in your preferences and will persist across
   sessions.

Maximum Log Lines
------------------

The log viewer will limit the number of lines displayed to prevent performance
issues with very large log files. The default limit is **5000 lines** per file,
with a maximum allowed limit of **50,000 lines**.

You can adjust this limit in your **User Profile** settings:

1. Click on your user profile icon in the top right of the GUI/web UI
2. Select "User Profile"
3. Find the "Maximum log lines" setting
4. Enter a new value (between 1 and 50,000)
5. The setting is automatically saved

The limit applies to all log files you view in the future. If a log file exceeds
this limit, a warning banner will appear at the top of the log viewer informing
you that the file has been truncated and which end was omitted.

.. warning::

   Setting a very high limit (e.g., 50,000 lines) may cause the web UI to
   become slow or unresponsive when loading large log files. Adjust this
   setting based on your system's performance.

Log File Truncation
--------------------

When a log file exceeds your configured maximum line limit, the log viewer will
truncate the display and show a warning banner indicating which end of the file
has been truncated:

- **In HEAD mode:** The end of the file is truncated (you see the beginning)
- **In TAIL mode:** The start of the file is truncated (you see the end)

The truncation banner displays:

- Which end of the file has been truncated (start or end)
- The maximum number of lines being displayed

This helps you understand what portion of the log file you're viewing and
whether you need to increase the line limit to see more content.

Other Log Viewer Controls
---------------------------

The log viewer toolbar provides additional controls:

**Timestamps**
   Toggle the display of timestamps for each log line (when available).

**Word Wrap**
   Toggle word wrapping for long lines to make them easier to read.

**Auto Scroll**
   When enabled (default in TAIL mode), automatically scroll to the newest
   lines as they arrive. You can disable this to manually browse the log
   without jumping to the end.

Accessing Log Files via Command Line
--------------------------------------

If you prefer to use the command line, you can view log files using the
``cylc cat-log`` command:

.. code-block:: bash

   # View the scheduler log for a workflow
   cylc cat-log <workflow>

   # View a job log file (follow from start)
   cylc cat-log <workflow>//<cycle>/<task>/<job> -f e

   # View the last N lines of a log file
   cylc cat-log <workflow> -f o --tail-lines 50

For more information on ``cylc cat-log``, see ``cylc cat-log --help``.
