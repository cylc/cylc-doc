Main Loop Plugins
=================

Main loop plugins allow you to run Python code inside a running
Cylc Flow scheduler.

https://docs.python.org/3/library/asyncio-task.html#coroutines


Built-In Plugins
----------------

Cylc Flow provides the following plugins:

.. autosummary::
   :toctree: built-in
   :template: main_loop_plugin.rst

   cylc.flow.main_loop.auto_restart
   cylc.flow.main_loop.health_check
   cylc.flow.main_loop.log_data_store
   cylc.flow.main_loop.log_main_loop
   cylc.flow.main_loop.log_memory

.. Note: Autosummary generates files in this directory, these are cleaned
         up by `make clean`.


Configuring
-----------

Main loop plugins can be activated either by:

* Calling `cylc run` or `cylc restart` `--main-loop` option
  e.g. `cylc run <SUITE> --main-loop 'health check'`
* Adding them to the default list of plugins in `[cylc][main loop]plugins`.

Main loop plugins can be individually configured in their
[cylc][main loop][__MANY__] section.


Developing Main Loop Plugins
----------------------------

Main loop plugins are Python modules containing asynchronous function(s)
(sometimes referred to as coroutines) which Cylc Flow executes within the
scheduler.

Here is the hello world example of a main loop plugin:

.. code-block:: python
   :caption: my_plugin.py

   from cylc.flow.main_loop import startup

   @startup
   async def my_startup_coroutine(schd, state):
      print(f'Hello {schd.suite}')

Plugins are registered by registering them with the `cylc.main_loop`
entry point:

.. code-block:: python
   :caption: setup.py

   setup(
       name='my-plugin',
       version='1.0',
       py_modules=['my_plugin'],
       entry_points={
          'cylc.main_loop': [
            # name = python.namespace.of.module
            'my_plugin=my_plugin.my_plugin'
          ]
       }


Event Types
-----------

The `cylc.flow.main_loop` module contains decorators for different events,
e.g. the `startup` decorator will cause a coroutine to be invoked on suite
startup.

.. autofunction:: cylc.flow.main_loop.startup

.. autofunction:: cylc.flow.main_loop.shutdown

.. autofunction:: cylc.flow.main_loop.periodic
