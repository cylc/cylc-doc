.. _UI_Server_config:

UI Server Configuration
=======================

Cylc UI Server can be configured using a ``jupyter_config.py``.

Site level configuration, such as ``c.CylcUIServer.site_authorization`` should
be defined in ``/etc/cylc/hub/jupyter_config.py``, or, alternatively, the
environment variable ``CYLC_SITE_CONF_PATH``.
User level configuration should be located in ``~/.cylc/hub/jupyter_config.py``.

.. automodule:: cylc.uiserver.app

.. autoconfigurable:: cylc.uiserver.app.CylcUIServer
    :inherited-members: False
