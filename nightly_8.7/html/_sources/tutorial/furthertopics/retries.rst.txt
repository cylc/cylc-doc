.. _tutorial.retries:

Retries
=======

.. seealso::

   :ref:`Cylc User Guide <TaskRetries>`

Retries allow us to automatically re-submit tasks which have failed due to
failure in submission or execution.


Purpose
-------

Retries can be useful for tasks that occasionally fail for known, fixable
reasons. Cylc can rerun a failing job multiple times, with user-defined delays
between tries.

Tasks that fail because of temporary hardware or network outages may succeed if
simply resubmitted after a delay. Others might succeed if configured differently
on the retry.

A job environment variable :envvar:`CYLC_TASK_TRY_NUMBER` increments with each
try, to allow try-dependent behaviour in the task script.

.. note::

   Tasks only enter the ``submit-failed`` state if job submission fails with no
   retries left. Otherwise they return to the waiting state, to wait on the
   next try.

   Tasks only enter the ``failed`` state if job execution fails with no retries
   left. Otherwise they return to the waiting state, to wait on the next try.


Example
-------

.. image:: https://upload.wikimedia.org/wikipedia/commons/7/73/Double-six-dice.jpg
   :width: 200px
   :align: right
   :alt: Two dice both showing the number six

Create a new workflow by running the following commands::

   mkdir -p ~/cylc-src/retries-tutorial
   cd ~/cylc-src/retries-tutorial

And paste the following code into a ``flow.cylc`` file. This workflow has a
``roll_doubles`` task that simulates trying to roll doubles using two dice:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = start => roll_doubles => win

   [runtime]
       [[start]]
       [[win]]
       [[roll_doubles]]
           script = """
               sleep 10
               RANDOM=$$  # Seed $RANDOM
               DIE_1=$((RANDOM%6 + 1))
               DIE_2=$((RANDOM%6 + 1))
               echo "Rolled $DIE_1 and $DIE_2..."
               if (($DIE_1 == $DIE_2)); then
                   echo "doubles!"
               else
                   exit 1
               fi
           """


Running Without Retries
-----------------------

Let's see what happens when we run the workflow as it is.
Look at the workflow with :ref:`tutorial.gui` or :ref:`tutorial.tui`

Then validate install and run the workflow::

   cylc validate .
   cylc install
   cylc play retries-tutorial

Unless you're lucky, the workflow should fail at the roll_doubles task.

Stop the workflow::

   cylc stop retries-tutorial


Configuring Retries
-------------------

We need to tell Cylc to retry it a few times. To do this, add the following
to the end of the ``[[roll_doubles]]`` task section in the :cylc:conf:`flow.cylc` file:

.. code-block:: cylc

   execution retry delays = 5*PT6S

This means that if the ``roll_doubles`` task fails, Cylc expects to
retry running it 5 times before finally failing. Each retry will have
a delay of 6 seconds.

We can apply multiple retry periods with the
`execution retry delays <[runtime][<namespace>]execution retry delays>` setting
by separating them with commas, e.g:

.. code-block:: cylc

   # If the task fails, wait 15 seconss, then retry it.
   # If the retry fails, wait a further 10 minutes, then retry it again.
   # If the second retry fails, wait a further 1 hour, then retry it again.
   # If the third retry fails, wait a further 3 hours, then retry it again.
   execution retry delays = PT15S, PT10M, PT1H, PT3H


Running With Retries
--------------------

Look at the workflow with :ref:`tutorial.gui` or :ref:`tutorial.tui`

Re-install and run the workflow::

   cylc validate .
   cylc install
   cylc play retries-tutorial

What you should see is Cylc retrying the ``roll_doubles`` task. Hopefully,
it will succeed (there is only about a 1 in 3 chance of every task
failing) and the workflow will continue.


Altering Behaviour
------------------

We can alter the behaviour of the task based on the number of retries, using
:envvar:`CYLC_TASK_TRY_NUMBER`.

Change the ``script`` setting for the ``roll_doubles`` task to this::

   sleep 10
   RANDOM=$$  # Seed $RANDOM
   DIE_1=$((RANDOM%6 + 1))
   DIE_2=$((RANDOM%6 + 1))
   echo "Rolled $DIE_1 and $DIE_2..."
   if (($DIE_1 == $DIE_2)); then
       echo "doubles!"
   elif (($CYLC_TASK_TRY_NUMBER >= 2)); then
       echo "look over there! ..."
       echo "doubles!"  # Cheat!
   else
       exit 1
   fi

If your workflow is still running, stop it, then run it again.

This time, the task should definitely succeed before the third retry.


Further Reading
---------------

* :ref:`Cylc User Guide <TaskRetries>`
* `[runtime][<namespace>]execution retry delays`.
* `[runtime][<namespace>]submission retry delays`.
