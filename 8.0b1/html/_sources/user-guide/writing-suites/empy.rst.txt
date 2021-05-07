.. _User Guide EmPy:

EmPy
====

In addition to Jinja2, Cylc supports EmPy template processor in suite
configurations. Similarly to Jinja2, EmPy provides variables, mathematical
expressions, loop control structures, conditional logic, etc., that are
expanded to generate the final suite configuration seen by Cylc. See the
`EmPy documentation <http://www.alcyone.com/software/empy>`_ for more
details on its templating features and how to use them.

.. note::

   EmPy is not included in the standard Cylc installation, if installing
   with ``pip`` run ``pip install cylc-flow[empy]`` to install this
   dependency.

.. TODO: update this when the conda instructions change

To enable EmPy place an ``empy`` hash-bang comment on the first line of
the flow.cylc file:

.. code-block:: cylc

   #!empy
   # ...

An example suite ``empy.cities`` demonstrating its use is shown below.
It is a translation of ``jinja2.cities`` example from
:ref:`User Guide Jinja2` and can be directly compared against it.

.. literalinclude:: ../../suites/empy/cities/flow.cylc
   :language: cylc

For basic usage the difference between Jinja2 and EmPy amounts to a different
markup syntax with little else to distinguish them. EmPy might be preferable,
however, in cases where more complicated processing logic have to be
implemented.

EmPy is a system for embedding Python expressions and statements in template
text. It makes the full power of Python language and its ecosystem easily
accessible from within the template. This might be desirable for several
reasons:

- No need to learn different language and its idiosyncrasies just for
  writing template logic.
- Availability of lambda functions, list and dictionary comprehensions
  can make template code smaller and more readable compared to Jinja2.
- Natural and straightforward integration with Python package ecosystem.
- No two-language barrier between writing template logic and processing
  extensions makes it easier to refactor and maintain the template code
  as its complexity grows - inline pieces of Python code can be
  gathered into subroutines and eventually into separate modules and
  packages in a seamless manner.
