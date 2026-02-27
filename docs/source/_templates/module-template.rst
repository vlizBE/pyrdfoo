{{ fullname | escape | underline}}

.. automodule:: {{ fullname }}

   {% block functions %}
   {% if functions %}
   .. rubric:: {{ _('Functions') }}

   {% for item in functions %}

   .. autofunction:: {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block classes %}
   {% if classes %}
   .. rubric:: {{ _('Classes') }}

   {% for item in classes %}

   .. autoclass:: {{ item }}()
      :members:
      :undoc-members:
      :inherited-members: RDF, BaseModel
      :exclude-members: model_config
      :member-order: bysource
      :show-inheritance:
   {%- endfor %}
   {% endif %}
   {% endblock %}
