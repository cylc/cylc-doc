.. _tutorial-cylc-family-triggers:

Family Triggers
===============

To reduce duplication in the :term:`graph` is is possible to write
:term:`dependencies <dependency>` using collections of tasks called
:term:`families <family>`).

This tutorial walks you through writing such dependencies using family
:term:`triggers <task trigger>`.


Explanation
-----------

Dependencies between tasks can be written using a :term:`qualifier` to describe
the :term:`task state` that the dependency refers to (e.g. ``succeed``
``fail``, etc). If a dependency does not use a qualifier then it is assumed
that the dependency refers to the ``succeed`` state e.g:

.. code-block:: cylc-graph

   bake_bread => sell_bread          # sell_bread is dependent on bake_bread succeeding.
   bake_bread:succeed => sell_bread?  # sell_bread is dependent on bake_bread succeeding.
   sell_bread:fail? => throw_away   # through_away is dependent on sell_bread failing.

The left-hand side of a :term:`dependency` (e.g. ``sell_bread:fail``) is
referred to as the :term:`trigger <task trigger>`.

.. versionchanged:: 8.0.0

   ``sell_bread(:succeed)`` and ``sell_bread:fail`` are mutually exclusive
   outcomes. To tell Cylc use the ``?`` syntax to mark them as
   :ref:`optional outputs`.

When we write a trigger involving a family, special qualifiers are required
to specify whether the dependency is concerned with *all* or *any* of the tasks
in that family reaching the desired :term:`state <task state>` e.g:

* ``succeed-all``
* ``succeed-any``
* ``fail-all``

Such :term:`triggers <task trigger>` are referred to as
:term:`family triggers <family trigger>`


Example
-------

Create a new workflow called ``tutorial-family-triggers``::

   mkdir ~/cylc-src/tutorial-family-triggers
   cd ~/cylc-src/tutorial-family-triggers

Paste the following configuration into the :cylc:conf:`flow.cylc` file:

.. code-block:: cylc

   [scheduler]
       UTC mode = True # Ignore DST
   [scheduling]
       [[graph]]
           R1 = visit_mine => MINERS
   [runtime]
       [[visit_mine]]
           script = sleep 5; echo 'off to work we go'

       [[MINERS]]
           script = """
               sleep 5;
               if (($RANDOM % 2)); then
                   echo 'Diamonds!'; true;
               else
                   echo 'Nothing...'; false;
               fi
           """
       [[doc, grumpy, sleepy, happy, bashful, sneezy, dopey]]
           inherit = MINERS

You have now created a workflow that:

* Has a ``visit_mine`` task that sleeps for 5 seconds then outputs a
  message.
* Contains a ``MINERS`` family with a command in it that randomly succeeds
  or fails.
* Has 7 tasks that inherit from the ``MINERS`` family.

Validate, install and run the workflow::

   cylc validate .
   cylc install
   cylc play tutorial-family-triggers

You should see the ``visit_mine`` task run, then trigger the members of the
``MINERS`` family. Note that some of the ``MINERS`` tasks may fail so you
will need to stop your workflow using the "stop" button in the UI, or::

   cylc stop tutorial-family-triggers


Family Triggering: Success
--------------------------

As you will have noticed by watching the workflow run, some of the tasks in the
``MINERS`` family succeed and some fail.

We would like to add a task to sell any diamonds we find, but wait for all
the miners to report back first so we only make the one trip.

We can address this by using *family triggers*. In particular, we are going
to use the ``finish-all`` trigger to check for all members of the ``MINERS``
family finishing, and the ``succeed-any`` trigger to check for any of the
tasks in the ``MINERS`` family succeeding.

Open your :cylc:conf:`flow.cylc` file and change the ``[[graph]]`` to look like
this:

.. code-block:: cylc

   [[graph]]
       R1 = """
           visit_mine => MINERS?
           MINERS:finish-all & MINERS:succeed-any? => sell_diamonds
       """

Then, add the following task to the ``[runtime]`` section:

.. code-block:: cylc

   [[sell_diamonds]]
      script = sleep 5

These changes add a ``sell_diamonds`` task to the workflow which is run once
all the ``MINERS`` tasks have finished and if any of them have succeeded.

Save your changes and run your workflow. You should see the new
``sell_diamonds`` task being run once all the miners have finished and at
least one of them has succeeded. Stop your workflow as described above.


Family Triggering: Failure
--------------------------

Cylc also allows us to trigger off failure of tasks in a particular family.

We would like to add another task to close down unproductive mineshafts once
all the miners have reported back and had time to discuss their findings.

To do this we will make use of family triggers in a similar manner to before.

Open your :cylc:conf:`flow.cylc` file and change the ``[[graph]]`` to look like
this:

.. code-block:: cylc

   [[graph]]
       R1 = """
           visit_mine => MINERS?
           MINERS:finish-all & MINERS:succeed-any? => sell_diamonds
           MINERS:finish-all & MINERS:fail-any? => close_shafts
       """

Alter the ``[[sell_diamonds]]`` section to look like this:

.. code-block:: cylc

   [[close_shafts, sell_diamonds]]
       script = sleep 5

These changes add a ``close_shafts`` task which is run once all the
``MINERS`` tasks have finished and any of them have failed.

Save your changes and run your workflow. You should see the new
``close_shafts`` run should any of the ``MINERS`` tasks be in the failed
state once they have all finished.


Different Triggers
------------------

Other family :term:`qualifiers <qualifier>` beyond those covered in the
example are also available.

The following types of "all" qualifier are available:

* ``:start-all`` - all the tasks in the family have started
* ``:succeed-all`` - all the tasks in the family have succeeded
* ``:fail-all`` - all the tasks in the family have failed
* ``:finish-all`` - all the tasks in the family have finished

The following types of "any" qualifier are available:

* ``:start-any`` - at least one task in the family has started
* ``:succeed-any`` - at least one task in the family has succeeded
* ``:fail-any`` - at least one task in the family has failed
* ``:finish-any`` - at least one task in the family has finished


Summary
-------

* Family triggers allow you to write dependencies for collections of tasks.
* Like :term:`task triggers <task trigger>`, family triggers can be based on
  success, failure, starting and finishing of tasks in a family.
* Family triggers can trigger off either *all* or *any* of the tasks in a
  family.
