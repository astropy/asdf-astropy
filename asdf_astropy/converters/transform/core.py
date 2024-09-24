import abc

from asdf.extension import Converter

from asdf_astropy.converters.utils import import_type


def parameter_to_value(param):
    """
    Convert a model parameter to a Quantity or number,
    depending on the presence of a unit.

    Parameters
    ----------
    param : astropy.modeling.Parameter

    Returns
    -------
    astropy.units.Quantity or float
    """
    from astropy import units as u

    if param.unit is not None:
        return u.Quantity(param)

    return param.value


# One converter, UnitsMappingConverter, does not inherit
# this class.  When adding features here consider also
# updating UnitsMappingConverter.
# This class is used by other packages, e.g., gwcs, to implement
# converters for custom models.  Keep that in mind when modifying
# this code.
class TransformConverterBase(Converter):
    """
    ABC for transform/model converters.  Handles common
    properties after concrete converter sets model-specific
    properties.
    """

    @abc.abstractmethod
    def to_yaml_tree_transform(self, model, tag, ctx):
        """
        Convert a model's parameters into a dict suitable
        for ASDF serialization.  Common model properties
        such as name and inverse will be handled by this
        base class.

        Parameters
        ----------
        model : astropy.modeling.Model
            The model instance to convert.
        tag : str
            The tag identifying the YAML type that `astropy.modeling.Model` should be
            converted into.
        ctx : asdf.asdf.SerializationContext
            The context of the current serialization request.

        Returns
        -------
        dict
            ASDF node.
        """

    @abc.abstractmethod
    def from_yaml_tree_transform(self, node, tag, ctx):
        """
        Convert an ASDF node into an instance of the appropriate
        model class.  The implementing class need only instantiate
        the model and set parameter values; common model properties
        such as name and inverse will be handled by this base class.

        Parameters
        ----------
        node : dict
            The ASDF node to convert.
        tag : str
            The tag identifying the YAML type of the node.
        ctx : asdf.asdf.SerializationContext
            The context of the current serialization request.

        Returns
        -------
        astropy.modeling.Model
            The resulting model instance.
        """

    def to_yaml_tree(self, model, tag, ctx):
        from astropy.modeling.core import CompoundModel

        node = self.to_yaml_tree_transform(model, tag, ctx)

        if model.name is not None:
            node["name"] = model.name

        node["inputs"] = list(model.inputs)
        node["outputs"] = list(model.outputs)

        # Don't bother serializing analytic inverses provided
        # by the model:
        if getattr(model, "_user_inverse", None) is not None:
            node["inverse"] = model._user_inverse

        self._serialize_bounding_box(model, node)

        # model / parameter constraints
        if not isinstance(model, CompoundModel):
            fixed_nondefaults = {k: f for k, f in model.fixed.items() if f}
            if fixed_nondefaults:
                node["fixed"] = fixed_nondefaults
            bounds_nondefaults = {k: b for k, b in model.bounds.items() if any(b)}
            if bounds_nondefaults:
                node["bounds"] = bounds_nondefaults

        # model input_units_equivalencies
        if not isinstance(model, CompoundModel) and model.input_units_equivalencies:
            node["input_units_equivalencies"] = model.input_units_equivalencies

        return node

    def _serialize_bounding_box(self, model, node):
        from astropy.modeling.bounding_box import CompoundBoundingBox, ModelBoundingBox

        # ignore any default bounding_box
        if (bbox := model._user_bounding_box) is not None:
            if isinstance(bbox, ModelBoundingBox):
                self._serialize_bbox(model, node)
            elif isinstance(bbox, CompoundBoundingBox):
                self._serialize_cbbox(model, node)

    def _serialize_bbox(self, model, node):
        from astropy.modeling.bounding_box import ModelBoundingBox

        bbox = model.bounding_box

        if len(bbox.ignored) > 0:
            kwargs = {"_preserve_ignore": True}
        else:
            kwargs = {}

        node["bounding_box"] = ModelBoundingBox.validate(model, bbox, **kwargs)

    def _serialize_cbbox(self, model, node):
        node["bounding_box"] = model.bounding_box

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.modeling.core import CompoundModel

        model = self.from_yaml_tree_transform(node, tag, ctx)

        if "name" in node:
            model.name = node["name"]

        if "inputs" in node:
            model.inputs = tuple(node["inputs"])

        if "outputs" in node:
            model.outputs = tuple(node["outputs"])

        self._deserialize_bounding_box(model, node)

        param_and_model_constraints = {}
        for constraint in ["fixed", "bounds"]:
            if constraint in node:
                param_and_model_constraints[constraint] = node[constraint]
        model._initialize_constraints(param_and_model_constraints)

        # this still writes eqs. for compound, but operates on each sub model
        if "input_units_equivalencies" in node and not isinstance(model, CompoundModel):
            model.input_units_equivalencies = node["input_units_equivalencies"]

        yield model

        if "inverse" in node:
            model.inverse = node["inverse"]

    def _deserialize_bounding_box(self, model, node):
        if "bounding_box" in node:
            bounding_box = node["bounding_box"]

            if isinstance(bounding_box, list):
                model.bounding_box = bounding_box
            elif callable(bounding_box):
                model.bounding_box = bounding_box(model)
            else:
                msg = f"Cannot form bounding_box from: {bounding_box}"
                raise TypeError(msg)


class SimpleTransformConverter(TransformConverterBase):
    """
    Class for converters that serialize all of a model's parameters
    and do not require special behavior based on tag version.

    Parameters
    ----------
    tags : list of str
        Tag patterns.

    model_type_name
        Fully-qualified model type name.
    """

    def __init__(self, tags, model_type_name):
        self._tags = tags
        self._model_type_name = model_type_name
        self._model_type = None

    @property
    def tags(self):
        return self._tags

    @property
    def types(self):
        return [self._model_type_name]

    @property
    def model_type(self):
        # Delay import until the model class is needed to improve speed
        # of loading the extension.
        if self._model_type is None:
            self._model_type = import_type(self._model_type_name)
        return self._model_type

    def to_yaml_tree_transform(self, model, tag, ctx):
        return {p: parameter_to_value(getattr(model, p)) for p in model.param_names}

    def from_yaml_tree_transform(self, node, tag, ctx):
        model_type = self.model_type
        model_kwargs = {}
        for param in model_type.param_names:
            if param in node:
                model_kwargs[param] = node[param]
        return model_type(**model_kwargs)
