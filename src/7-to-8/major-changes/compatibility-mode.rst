.. _cylc_7_compat_mode:

Cylc 7 Compatibility Mode
=========================

Cylc 8 initially provided a Cylc 7 compatibility mode which allowed workflows
to be run under either Cylc 7 or 8, to help facilitate migration.

This compatibility mode was removed in Cylc 8.7.0. If you have any workflows
that still use a ``suite.rc`` file, please skim through
:ref:`configuration-changes` then rename this file to ``flow.cylc`` and address
any errors/warnings.

For more information on what compatibility mode did, please see the
`Cylc 8.6 documentation <https://cylc.github.io/cylc-doc/8.6.3/html/7-to-8/major-changes/compatibility-mode.html>`_.
