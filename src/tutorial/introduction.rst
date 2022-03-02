.. _cylc-introduction:

Introduction
============

.. _cylc-what-is-a-workflow:

What Is A Workflow?
-------------------

.. epigraph::

   A workflow consists of an orchestrated and repeatable pattern of business
   activity enabled by the systematic organization of resources into processes
   that transform materials, provide services, or process information.

   -- Wikipedia

.. ifnotslides::

   In research, business and other fields we may need to repeat processes in
   the course of our work. At its simplest a workflow is a set of steps that
   must be followed in a particular order to achieve some end goal.

   We can represent each "step" in a workflow as a node in a graph, and the
   order with arrows between them.

.. nextslide::

.. digraph:: bakery
   :align: center

   "purchase ingredients" -> "make dough" -> "bake bread" -> "sell bread"
   "bake bread" -> "clean oven"
   "pre-heat oven" -> "bake bread"


.. _cylc-what-is-cylc:

What Is Cylc?
-------------

.. ifnotslides::

   Cylc (pronounced silk) is a workflow engine, a system that automatically
   executes tasks according to schedules and dependencies.

   In a Cylc workflow each step is a computational task that runs a script or
   application of some kind. Cylc runs each task as soon as it is appropriate
   to do so.

.. minicylc::
   :align: center
   :theme: demo

    a => b => c
    b => d => f
    e => f

.. nextslide::

Cylc can automatically:

- Submit tasks across computer systems and resource managers.
- Recover from failures.
- Repeat workflows.

.. ifnotslides::

   Cylc was originally developed at NIWA (The National Institute of Water and
   Atmospheric Research, New Zealand) for running their weather forecasting
   workflows. It is now developed by an international partnership including
   NIWA, the Met Office (UK), and members of the Unified Model Consortium.
   Though initially developed for meteorological purposes Cylc is a general
   purpose tool as applicable in business as it is in scientific research.

.. nextslide::

.. ifslides::

   * Originally developed at NIWA (New Zealand)
   * Now developed by an international partnership including the
     Met Office (UK).
   * General purpose tool as applicable in business as in
     scientific research.

.. nextslide::

Cylc provides a variety of command line and GUI tools for visualising,
monitoring, and controlling workflows. The Cylc TUI (Terminal
User Interface), web GUI, and ``cylc scan`` (bottom left) are shown below.

.. image:: /tutorial/img/cylc-tools.png
   :alt: A screenshot of several Cylc tools.

.. nextslide::

.. ifslides::

   :ref:`tutorial-cylc-graphing`
