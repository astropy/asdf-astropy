.. _basic_example:

=======
Example
=======


In this example, we will show how to implement serialization for a new
`~astropy.modeling.Model` object, but the basic principles apply to
serialization of other **astropy** objects. As mentioned, adding a new object
to **asdf-astropy** requires both a tag and a converter.

Creating the Tag
----------------

All of the tags for transforms (**astropy** models) are currently defined within
the :ref:`asdf-transform-schemas <asdf-transform-schemas:asdf-transform-schemas>`,
along side the schemas which compose them.  Any new serializable **astropy** model
will require the creation of a new tag, which will likely require the creation of
a new schema.

Let's consider a new model called ``MyModel``, a new model in ``astropy.modeling.functional_models``
that has two parameters ``amplitude`` and ``x_0``. We would like to strictly require both
of these parameters be set. We would also like to specify that these parameters can
either be numeric type, or ``astropy.units.quantity`` type. A schema describing this
model would look like

.. code-block:: yaml

    %YAML 1.1
    ---
    $schema: "http://stsci.edu/schemas/yaml-schema/draft-01"
    id: "http://astropy.org/schemas/mymodel-1.0.0"
    title: >
      Example New Model.

    description: >
      Example new model, which describes the distribution of ABC.

    allOf:
      - $ref: "transform-1.2.0"
      - type: object
        properties:
          amplitude:
            anyOf:
              - tag: tag:stsci.edu:asdf/unit/quantity-1.1.0
              - type: number
            description: Amplitude of distribution.
          x_0:
            anyOf:
              - tag: tag:stsci.edu:asdf/unit/quantity-1.1.0
              - type: number
            description: X center position.

        required: ['amplitude', 'x_0]
    ...

All new transform schemas reference the base transform schema with the latest
version. This schema describes the other model attributes that are common to all
or many models, so that individual schemas only handle the parameters specific
to that model. Additionally, this schema uses the latest tag for ``quantity``,
so that models can retain information about units and quantities. References allow
previously defined schemas to be used inside new custom types, while the direct
reference to a specific tag is preferred when possible as this allows ASDF to more
confidently validate both the schema itself and the ASDF files which make use of it.

Finally, we can create the **tag** itself. This is done by creating an entry in a
manifest for the tag. The manifest entry is where the **tag** gets associated with the
schemas that are used by **ASDF** to validate the ASDF file. An example manifest
entry for this model would look something like:

.. code-block:: yaml

    - tag_uri: tag:stsci.edu:asdf/transform/mymodel-1.0.0
      schema_uri: http://astropy.org/schemas/mymodel-1.0.0
      title: Example New Model
      description: |-
          Example new model, which describes the distribution of ABC.

If one was contributing this tag to **asdf-astropy**, this entry would be
added the :ref:`asdf-astropy_manifest` directly. Doing this will allow
**asdf-astropy** to properly register this tag and associate this tag with its underlying
schema for use by **ASDF**. Moreover, the underlying schema will need to be added to the
``asdf_astropy/resources/schemas`` directly in order for **asdf-astropy** to make
use of it when creating the tag in **ASDF**.

.. note::

    This is not a complete manifest, instead it is a listing for a single
    tag for a manifest. See :ref:`asdf-astropy_manifest` for an example of
    a complete manifest. Moreover, a manifest is not strictly the only way
    to create a tag for ASDF (this can be done using the ASDF context manager
    for example); however, it is the standard way to create a tag for ASDF
    for use with a given package.

Creating a Converter
--------------------

The next component for enabling ASDF to serialize and deserialize an object
is to create a **converter** class.

.. note::
    For most transforms the
    `asdf_astropy.converters.transform.core.SimpleTransformConverter` will be sufficient
    to construct the necessary converter for your model. However, for completeness
    we will describe the general procedure for writing both a transform converter
    and a more general converter.

Creating a Transform Converter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If we want to use the **asdf-astropy** framework for writing transform converters; namely, using
`asdf_astropy.converters.transform.core.TransformConverterBase`, we need to define two methods
``to_yaml_tree_transform`` and ``from_yaml_tree_transform``. The ``to_yaml_tree_transform``
will perform the serialization of the parts of ``MyModel`` which are specific to ``MyModel``,
while ``from_yaml_tree_transform`` will perform the deserialization of the parts of
``MyModel`` specific to ``MyModel``. Moreover, the converter class must also
specify the ``tags`` corresponding to ``MyModel`` and the matching Python `types` for
those ``tags``. The ``tags`` are what **ASDF** uses to identify which converter to use when
deserializing an ASDF file, while the `types` are used by **ASDF** to identify which converter
to use when serializing an object to an ASDF file.::

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

If one was contributing this converter to **asdf-astropy**, this class would
need to be instantiated and then added to the ``TRANSFORM_CONVERTERS`` list
in the `asdf_astropy.extensions` module. By doing this **asdf-astropy**
will be able to properly register this converter with **ASDF** so that it
can be used seamlessly when working with **ASDF**.

Creating a General Converter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If one needs to create a more general (e.g. non-transform) converter, say
``MyType``, then one will need to inherit from `asdf.extension.Converter`.
In this case ``tags`` and `types` must still be defined, but instead
``to_yaml_tree`` and ``from_yaml_tree`` must be defined instead::

    from asdf.extension import Converter

    class MyTypeConverter(Converter):
        tags = ["tag:<tag for MyType"]
        types = ["<Python import for MyType>"]

        def to_yaml_tree(self, obj, tag, ctx):
            """Code to create a Python dictionary representing MyType"""
            ...

        def from_yaml_tree(self, node, tag, ctx):
            """Code to read a Python dictionary representing MyType"""
            ...

For more details please see :ref:`asdf:extending_extensions`.
