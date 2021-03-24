{{ fullname | escape | underline }}

.. automodule:: {{ fullname }}
   :members: {{ functions | join(', ') }}

   .. set members so that we only document what is actually defined
      otherwise you can end up with imported modules and mess like that

   {% block functions %}

   Python API
   ----------

   {% if functions %}
   .. rubric:: Coroutines

   .. write out a table of functions (coroutines in this context)
      for quick reference
       
   .. autosummary::
      :nosignatures:

   {% for item in functions %}
      {{ item }}
   {%- endfor %}

   {% endif %}
   {% endblock %}
