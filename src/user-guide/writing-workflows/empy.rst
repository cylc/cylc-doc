.. _User Guide EmPy:

EmPy
====

Cylc also supports the EmPy template processor in workflow configurations.
Like :ref:`User Guide Jinja2`, EmPy provides variables, mathematical
expressions, loop control structures, conditional logic, etc., that gets
expanded to generate the final workflow configuration seen - which must must be
valid Cylc syntax. See `EmPy documentation
<http://www.alcyone.com/software/empy>`_ for details of its templating features
and how to use them.

.. note::

   EmPy is not included in the standard Cylc installation. If installing
   with ``pip`` run ``pip install cylc-flow[empy]`` to install it.

.. TODO: update this when the conda instructions change

To enable EmPy place an ``empy`` hash-bang comment on the first line of
the ``flow.cylc`` file:

.. code-block:: cylc

   #!empy


As an example, here is the "cities" workflow from the previous section,
implemented with Empy instead of Jinja2.

.. literalinclude:: ../../workflows/empy/cities/flow.cylc
   :language: cylc

For basic usage, the difference between Jinja2 and EmPy amounts to little more than
a different markup syntax. EmPy might be preferable, however, in cases needing
more complicated processing logic.

*EmPy is a system for embedding Python expressions and statements in template
text. It makes the full power of Python language and its ecosystem easily
accessible from within the template. This might be desirable for several
reasons:*

- No need to learn a different language just for writing template logic
- Availability of lambda functions, lists, and dictionary comprehensions
  can make template code smaller and more readable compared to Jinja2
- Natural and straightforward integration with the Python package ecosystem
- No two-language barrier between writing template logic and processing
  extensions makes it easier to refactor and maintain the template code
  as its complexity grows. Inline Python code can be gathered into subroutines
  and eventually into separate modules and packages in a seamless manner.
