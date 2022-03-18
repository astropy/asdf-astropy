.. _basic_example:

=======
Example
=======


In this example, we will show how to implement serialization for a new
`~astropy.modeling.Model` object, but the basic principles apply to
serialization of other ``astropy`` objects. As mentioned, adding a new object
to ``asdf-astropy`` requires both a converter and a tagged-schema.

All schemas for transforms are currently defined within the asdf-transform-schemas.
Any new serializable transforms can have a corresponding new schema here. Let's
consider a new model called ``MyModel``, a new model in ``astropy.modeling.functional_models``
that has two parameters ``amplitude`` and ``x_0``. We would like to strictly require both
of these parameters be set. We would also like to specify that these parameters can
either be numeric type, or ``astropy.units.quantity`` type. A schema describing this
model would look like

.. code-block:: yaml

    %YAML 1.1
    ---
    $schema: "http://stsci.edu/schemas/yaml-schema/draft-01"
    id: "http://stsci.edu/schemas/asdf/transform/mymodel-1.0.0"
    tag: "tag:stsci.edu:asdf/transform/mymodel-1.0.0"
    title: >
      Example new model.

    description: >
      Example new model, which describes the distribution of ABC.

    allOf:
      - $ref: "transform-1.2.0"
      - type: object
        properties:
          amplitude:
            anyOf:
              - $ref: "../unit/quantity-1.1.0"
              - type: number
            description: Amplitude of distribution.
          x_0:
            anyOf:
              - $ref: "../unit/quantity-1.1.0"
              - type: number
            description: X center position.

        required: ['amplitude', 'x_0]
    ...

.. note::
   The presence of the ``tag:`` attribute in the schema is what keys ASDF
   into using the correct converter when serialization and deserialization
   are preformed.


All new transform schemas reference the base transform schema of the latest
type. This schema describes the other model attributes that are common to all
or many models, so that individual schemas only handle the parameters specific
to that model. Additionally, this schema references the latest version
of the ``quantity`` schema, so that models can retain information about units
and quantities. References allow previously defined objects to be used inside
new custom types.

.. note::
    For most transforms the
    `~asdf_astropy.converters.transform.core.SimpleTransformConverter` will be sufficient
    to construct the necessary converter for your model. However, for completeness
    we will describe the general procedure for writing both a transform converter
    and a general converter.

The next component is the converter class. If we want to use the ``asdf-astropy``
framework for writing transform converters; namely, using
`~asdf_astropy.converters.transform.core.TransformConverterBase``, we need to define two methods
``to_yaml_tree_transform`` and ``from_yaml_tree_transform``. The ``to_yaml_tree_transform``
will perform the serialization of the parts of ``MyModel`` which are specific to ``MyModel``,
while ``from_yaml_tree_transform`` will perform the deserialization of the parts of
``MyModel`` specific to ``MyModel``. Moreover, the converter class must also
specify the `tags` for the schemas corresponding to ``MyModel`` and the matching `types` for
those schemas::

    from asdf_astropy.converters.transform.core import TransformConverterBase, parameter_to_value

    class MyModelConverter(TransformConverterBase):
        tags = ["tag:stsci.edu:asdf/transform/mymodel-1.0.0"]
        types = ['astropy.modeling.functional_models.MyModel']

        def to_yaml_tree_transform(self, model, tag, ctx):
            node = {'amplitude': parameter_to_value(amplitude),
                    'x_0': parameter_to_value(x_0)}
            return node

        def from_yaml_tree_transform(self, node, tag, ctx):
            from astropy.modeling.functional_models import MyModel

            return MyModel(amplitude=node['amplitude'], x_0=node['x_0'])


If one needs to create a more general (e.g. non-transform) converter, say
``MyType``, then one will need to inherit from `asdf.extension.Converter`.
In this case `tags` and `types` must still be defined, but instead
``to_yaml_tree`` and ``from_yaml_tree`` must be defined instead::

    from asdf.extension import Converter

    class MyTypeConverter(Converter):
        tags = ["tag:<tag for MyType"]
        types = ["<python import for MyType>"]

        def to_yaml_tree(self, obj, tag, ctx):
            """Code to create a python dictionary representing MyType"""
            ...

        def from_yaml_tree(self, node, tag, ctx):
            """Code to read a python dictionary representing MyType"""
            ...

For more details please see `Writing ASDF Extensions <https://asdf.readthedocs.io/en/latest/asdf/extending/extensions.html>`_.
