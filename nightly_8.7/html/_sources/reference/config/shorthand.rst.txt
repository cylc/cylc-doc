In the documentation, we often use a compact single-line notation to refer to
nested config items, where we drop the additional brackets at each level:

``[section]``
   An entire section.
``[section]setting``
   A setting within a section.
``[section]setting=value``
   The value of a setting within a section.
``[section][sub section]another setting``
   A setting within a sub-section.

This is purely for making it easier to refer to items; they cannot be written
this way in the ``flow.cylc`` file.
