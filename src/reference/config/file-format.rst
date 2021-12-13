.. _file-format:

The .cylc File Format
=====================

Cylc global and workflow configuration files are written in a nested
`INI`_-based format.

.. _syntax:

Syntax
------

Comments
   Comments follow a ``#`` character.

Settings
   Configuration items (settings) are written as ``key = value`` pairs, and can
   be contained within sections. Setting names (the keys) may contain spaces.

String Values
   Quoting single-line string values is optional:

   .. code-block:: cylc

      [animals]
         cat = dusty
         dog = "fido"  # or single quotes: 'fido'

   Multiline string values must be triple-quoted:

   .. code-block:: cylc

      [song]
         lyrics = """  # (or triple single-quotes: '''value''')
            No stop signs
            Speed limit
            Nobody's gonna slow me down
         """

List Values
   List values are comma-separated:

   .. code-block:: cylc

      animals = dusty, fido, cujo


Boolean Values
   Booleans are capitalized:

   .. code-block:: cylc

      ice cream is good = True  # or False


Sections and Sub-sections
   Settings have a level-dependendent number of square brackets:

   .. code-block:: cylc

      [section]
      [[sub-section]]
      [[[sub-sub-section]]]


Indentation
   It is advisable to indent sections and subsections, for clarity. However,
   Cylc ignores indentation, so this:

   .. code-block:: cylc

      [section]
         a = A
         [[sub-section]]
            b = B
         b = C  # WARNING: this is still in sub-section!

   is equivalent to this:

   .. code-block:: cylc

      [section]
         a = A
         [[sub-section]]
            b = C


Duplicate Sections and Items
   Duplicate sections get merged into one. Duplicate settings overwrite
   previously defined values. So this:

   .. code-block:: cylc

      [animals]
        cat = fluffy
      [animals]
        dog = fido
        cat = dusty
 
   is equivalent to this:

   .. code-block:: cylc

      [animals]
        cat = dusty
        dog = fido


   The only exception to this rule is :term:`graph strings <graph string>`,
   which get merged. So these graph strings:

   .. code-block:: cylc-graph

      R1 = "foo => bar"
      R1 = "foo => baz"

   merge to this:

   .. code-block:: cylc-graph

      R1 = "foo => bar & baz"


Continuation lines
   If necessary, you can continue on the next line after a backslash character:

   .. code-block:: cylc

      verse = "the quick \
               brown fox"

   However, backslash line continuation is fragile (trailing invisible
   whitespace breaks it). Long :term:`graph strings <graph string>` strings
   should be split on graph symbols instead:

   .. code-block:: cylc-graph

      R1 = """
           (foo & bar ) |
               baz =>
                   qux
      """
      # Equivalent to:
      R1 = """
           (foo & bar ) | baz => qux
      """

Include-files
   ``flow.cylc`` fragments can be included verbatim with the ``%include``
   directive. Include-files can be included multiple times, and even nested.
   Include-file paths should relative to the ``flow.cylc`` location:

   .. code-block::

      %include "inc/site-a.cylc"

   :ref:`Jinja2's <Jinja>` template inclusion mechanism can be used with Cylc
   too.


Shorthand
---------

Throughout the documentation we refer to configuration settings in the
following way:

``[section]``
   An entire section.
``[section]setting``
   A setting within a section.
``[section]setting=value``
   The value of a setting within a section.
``[section][sub-section]another-setting``
   A setting within a sub-section.

.. warning::
   We only use one set of square brackets at each level when writing nested
   sections on one line like this. But in the file, each sub-section
   gets additional square brackets as shown above.
