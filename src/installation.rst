.. _Requirements:

Installation
============

Cylc runs on Linux. It is tested quite thoroughly on modern RHEL and Ubuntu
distros. Some users have also managed to make it work on other Unix variants
including Apple OS X, but they are not officially tested and supported.

Third-Party Software Packages
-----------------------------

.. _GNU Coreutils: https://www.gnu.org/software/coreutils/coreutils.html

Requirements:

- Python 3.7+

  - `python-jose <https://pypi.org/project/python-jose/>`_
  - `zmq <https://pypi.org/project/zmq/>`_
  - `colorama <https://pypi.org/project/colorama/>`_

- `GNU Coreutils`_

  - These must be available in the Cylc environment using the canonical names
    (e.g. ``ls``).

The following packages are necessary for running tests in Cylc:

- `pytest <https://pytest.org>`_

To generate the HTML User Guide, you will need:

- `Sphinx <http://www.sphinx-doc.org/en/master/>`_ 2.0+.


.. TODO: Remove or fix this section once deployment has been sorted.

To check that dependencies are installed and environment is configured
correctly run ``cylc check-software``:

.. code-block:: none

   $ cylc check-software
   Checking your software...

   Individual results:
   ================================================================================
   Package (version requirements)                           Outcome (version found)
   ================================================================================
                                 *REQUIRED SOFTWARE*
   Python (3+).............................FOUND & min. version MET (3.7.2.final.0)
   Python:zmq (any)..................................................FOUND (17.1.2)
   Python:jose (any)..................................................FOUND (2.0.2)
   Python:colorama (any)..............................................FOUND (0.4.1)

                 *OPTIONAL SOFTWARE for the configuration templating*
   Python:EmPy (any)..................................................FOUND (3.3.2)

                    *OPTIONAL SOFTWARE for the HTML documentation*
   Python:sphinx (1.5.3+)..........................FOUND & min. version MET (1.8.4)
   ================================================================================

   Summary:
                             ****************************
                                Core requirements: ok
                                Full-functionality: ok
                             ****************************


If errors are reported then the packages concerned are either not installed or
not in your Python search path.

.. note::

   ``cylc check-software`` has become quite trivial as we've removed or
   bundled some former dependencies, but in future we intend to make it
   print a comprehensive list of library versions etc. to include in with
   bug reports.

To check for specific packages only, supply these as arguments to the
``check-software`` command, either in the form used in the output of
the bare command, without any parent package prefix and colon, or
alternatively all in lower-case, should the given form contain capitals. For
example:

.. code-block:: bash

   $ cylc check-software graphviz Python urllib3

With arguments, check-software provides an exit status indicating a
collective pass (zero) or a failure of that number of packages to satisfy
the requirements (non-zero integer).

.. _InstallCylc:

Installing Cylc
---------------

Cylc releases can be downloaded from `GitHub
<https://cylc.github.io/cylc-flow>`_.

The wrapper script ``usr/bin/cylc`` should be installed to
the system executable search path (e.g. ``/usr/local/bin/``) and
modified slightly to point to a location such as ``/opt`` where
successive Cylc releases will be unpacked side by side.

To install Cylc, unpack the release tarball in the right location, e.g.
``/opt/cylc-7.7.0``, type ``make`` inside the release
directory, and set site defaults - if necessary - in a site global config file
(below).

Make a symbolic link from ``cylc`` to the latest installed version:
``ln -s /opt/cylc-7.7.0 /opt/cylc``. This will be invoked by the
central wrapper if a specific version is not requested. Otherwise, the
wrapper will attempt to invoke the Cylc version specified in
``$CYLC_VERSION``, e.g. ``CYLC_VERSION=7.7.0``. This variable
is automatically set in task job scripts to ensure that jobs use the same Cylc
version as their parent suite server program.  It can also be set by users,
manually or in login scripts, to fix the Cylc version in their environment.

Installing subsequent releases is just a matter of unpacking the new tarballs
next to the previous releases, running ``make`` in them, and copying
in (possibly with modifications) the previous site global config file.


.. _LocalInstall:

Local User Installation
^^^^^^^^^^^^^^^^^^^^^^^

It is easy to install Cylc under your own user account if you don't have
root or sudo access to the system: just put the central Cylc wrapper in
``$HOME/bin/`` (making sure that is in your ``$PATH``) and
modify it to point to a directory such as ``$HOME/cylc/`` where you
will unpack and install release tarballs. Local installation of third party
dependencies like Graphviz is also possible, but that depends on the particular
installation methods used and is outside of the scope of this document.

Create A Site Config File
^^^^^^^^^^^^^^^^^^^^^^^^^

Site and user global config files define some important parameters that affect
all suites, some of which may need to be customized for your site.
See :ref:`SiteAndUserConfiguration` for how to generate an initial site file and
where to install it. All legal site and user global config items are defined
in :ref:`SiteRCReference`.


.. _Configure Site Environment on Job Hosts:

Configure Site Environment on Job Hosts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Task jobs need access to Cylc on job hosts, to run task message (and other)
Cylc commands. Task job scripts invoke ``bash -l`` (login shells) to run the
job, so sites and users should ensure that their bash login scripts configure
the environment appropriately for access to Cylc. See
:ref:`HowTasksGetAccessToCylc` for more on job environment configuration.
