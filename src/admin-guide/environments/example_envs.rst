Example Environments
====================

A set of possible installations of Cylc:

.. csv-table::
   :header-rows:1
   
   environment, cylc, cylc uiserver, rose, install latest from github
   `Cylc 8 basic`_, ✔️, , ,
   `Cylc 8 with UI Server`_, ✔️,✔️, ,
   `Cylc 8 with Rose`_, ✔️,✔️,✔️,
   `Cylc 8 basic live from github`_, ✔️, , ,✔️
   `Cylc 8 with rose and GUI live from github`_,✔️,✔️,✔️,✔️

Example installation command:

.. code-block:: bash

   conda env create -f path/to/env.yml --name "name of env"

Cylc 8 basic
------------

Also demonstrates using different versions of Python.

.. literalinclude:: basic-3.7.yml
   :language: YAML


.. literalinclude:: basic-3.8.yml
   :language: YAML


.. literalinclude:: basic-3.9.yml
   :language: YAML

Cylc 8 with UI Server
---------------------

.. literalinclude:: gui.yml
   :language: YAML

Cylc 8 with Rose
----------------

.. literalinclude:: rose.yml
   :language: YAML

Cylc 8 basic live from github
-----------------------------

.. literalinclude:: live-basic.yml
   :language: YAML

Cylc 8 with rose and GUI live from github
-----------------------------------------

.. literalinclude:: live-full.yml
   :language: YAML
