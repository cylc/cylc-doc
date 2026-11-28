Parameters
==========

.. admonition:: does this change affect me?
   :class: tip

   If you use Cylc parameters with negative offsets (e.g. ``foo<x-1>``).


Overview
--------

There has been a subtle change in the way negative offsets are handled in parameters.


Example
-------

If you have a parameter ``x`` with the values 1, 2 & 3:

.. code-block:: cylc

   [task parameters]
      x = 1..3

And use it like so:

.. code-block:: cylc-graph

   a<x-1> => b<x> => c<x>

There is some ambiguity about how this should be interpreted when ``x=1``
because ``<x-1>`` would be ``0`` which is not a valid value for the parameter
``x``.

Cylc 7 removed the part of the expression which was out of range resulting in a
partial evaluation of that line:

.. code-block:: cylc-graph

           b_x1 => c_x1  # x=1
   a_x1 => b_x2 => c_x2  # x=2
   a_x2 => b_x3 => c_x3  # x=3

Whereas Cylc 8 will remove everything after the first out-of-range parameter - ``<x-1>`` (so the entire line for this example):

.. code-block:: cylc-graph

   a_x1 => b_x2 => c_x2  # x=2
   a_x2 => b_x2 => c_x2  # x=3


Migration
---------

If your workflow depends on the Cylc 7 behaviour, then the solution is
to break the expression into two parts which Cylc will then evaluate separately.

.. code-block:: diff

   - a<x-1> => b<x> => c<x>
   + a<x-1> => b<x>
   + b<x> => c<x>

Resulting in:

.. code-block:: cylc-graph
   
   # a<x-1> => b<x>
   a_x1 => a_x2  # x=2
   a_x2 => a_x3  # x=3

   # b<x> => c<x> 
   b_x1 => c_x1  # x=1
   b_x2 => c_x2  # x=2
   b_x3 => c_x3  # x=3


Line Breaks
-----------

Note that these expressions are all equivalent:

.. list-table::
   :class: grid-table

   * - .. code-block::

          a<x-1> => b<x> => c<x>

     - .. code-block::

          a<x-1> =>
          b<x> =>
          c<x>

     - .. code-block::

          a<x-1> => b<x> => \
          c<x>
