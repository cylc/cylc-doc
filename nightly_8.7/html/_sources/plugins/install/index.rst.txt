Pre-Configure And Post-Install Plugins
======================================

Pre-configure plugins allow Cylc to take additional actions before running
Cylc utilities such as ``cylc install``, ``cylc graph`` and ``cylc config``.

Post-install plugins allow Cylc to take additional actions after
running ``cylc install``.


Built In Plugins
----------------

Cylc Flow provides the following pre-configure and post-install plugins:

.. autosummary::
   :toctree: built-in
   :template: docstring_only.rst

   cylc.flow.install_plugins.log_vc_info

.. Note: Autosummary generates files in this directory, these are cleaned
         up by `make clean`.

Developing ``pre_configure`` and ``post_install`` plugins
---------------------------------------------------------

Cylc uses entry points registered by setuptools to search for pre-configure
and post-install plugins.

Hello World
^^^^^^^^^^^

In this example a pre-configure plugin which logs a "Hello World" message
and, after installation, logs some info about the installation:

.. code-block:: python
   :caption: ``my_plugin.py``

   from cylc.flow import LOG

   def pre_configure(srcdir=None, opts=None, rundir=None):
       # write Hello to the Cylc log.
       LOG.info(f'Hello World')
       return {}

   def post_install(srcdir=None, opts=None, rundir=None):
       LOG.info(f'installed from {srcdir}')
       LOG.info(f'installed to {rundir}')
       LOG.info(f'installation options were {options}')
       return {}

Plugins are registered by registering them with the ``cylc.pre_configure``
and ``cylc.post_install`` entry points:

.. code-block:: python
   :caption: ``setup.py``

   # plugins must be properly installed, in-place PYTHONPATH meddling will
   # not work.

   from setuptools import setup

   setup(
       name='my-plugin',
       version='1.0',
       py_modules=['my_plugin'],
       entry_points={
           # register this plugin with Cylc
           'cylc.pre_configure': [
           # name = python.namespace.of.module
           'my_plugin=my_plugin.my_plugin:pre_configure'
           ]
           'cylc.post_install': [
           # name = python.namespace.of.module
           'my_plugin=my_plugin.my_plugin:post_install'
           ]
       }
   )

API Reference
^^^^^^^^^^^^^

Cylc will pass following arguments to pre-configure and post-install plugins:

``srcdir`` (Path or string)
   The directory from which ``cylc install`` is installing a workflow,
   or the directory passed to ``cylc validate``, ``cylc graph`` and other
   CLI commands which work without installing a workflow.
``opts`` (``optparse.Values``)
   CLI options set for a Cylc script.
``rundir`` (Path or string)
   The destination of a ``cylc install`` or ``reinstall`` command.

The pre-configure plugin should return a dictionary which may contain the
following keys:

``env``
   A dictionary of environment variables to be exported to the scheduler
   environment.
``template_variables``
   A dictionary of template variables to be used by Jinja2 when
   templating the workflow configuration files.
``templating_detected``
   ``jinja2`` to be used when templating. N.b: This will result in
   failure if the templating language set does not match the shebang line of
   the ``flow.cylc`` file.

The post-install entry point does not return any data used by Cylc.

More advanced example
^^^^^^^^^^^^^^^^^^^^^

.. seealso::

   For the implementation of a more fully featured "real-world" example see
   :ref:`Cylc Rose`.

The example below looks for a file in the workflow source directory called
``template.json`` and activates if it exists.

At ``pre_configure`` template variables are extracted from a ``template.json``
file and provided to Cylc as both template and environment variables.

At ``post_install`` an additional log file is provided recording the version
of this plugin used.

.. code-block:: python
   :caption: An example json reading plugin

   import json
   from pathlib import Path

   VERSION = '0.0.1'

   def pre_configure(srcdir=None, opts=None, rundir=None):
       # Look for a 'template.json' file in the srcdir and make template
       # variables from it available as jinja2.
       template_file = (Path(srcdir) / 'template.json')

       # Trigger the plugin if some condition is met:
       if (template_file).exists():
           # You could retrieve info from a file:
           template = json.loads(template_file.read_text())

           # You can add variables programmatically:
           template['plugin_set_var'] = str(__file__)

           # Return a dict:
           return {
               'env': template,
               'template_variables': template,
               'templating_detected': 'jinja2'
           }
       else:
           return {}

   def post_install(srcdir=None, opts=None, rundir=None):
       # record plugin version in a file
       (Path(rundir) / 'log/json-plugin.info').write_text(
           f"Installed with Simple JSON reader plugin version {VERSION}\\n")
       return None
