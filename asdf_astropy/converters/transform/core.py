import abc

from asdf.extension import Converter

from ..utils import import_type


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
    else:
        return param.value


# One converter, UnitsMappingConverter, does not inherit
# this class.  When adding features here consider also
# updating UnitsMappingConverter.
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
            The tag identifying the YAML type that `model` should be
            converted into.
        ctx : asdf.asdf.SerializationContext
            The context of the current serialization request.

        Returns
        -------
        dict
            ASDF node.
        """
        pass  # pragma: no cover

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
        pass  # pragma: no cover

    def to_yaml_tree(self, model, tag, ctx):
        from astropy.modeling.core import CompoundModel

        node = self.to_yaml_tree_transform(model, tag, ctx)

        if model.name is not None:
            node["name"] = model.name

        # Don't bother serializing analytic inverses provided
        # by the model:
        if getattr(model, "_user_inverse", None) is not None:
            node["inverse"] = model._user_inverse

        try:
            bb = model.bounding_box
        except NotImplementedError:
            bb = None

        if bb is not None:
            if model.n_inputs == 1:
                node["bounding_box"] = list(bb)
            else:
                node["bounding_box"] = [list(item) for item in bb]

        # model / parameter constraints
        if not isinstance(model, CompoundModel):
            fixed_nondefaults = {k: f for k, f in model.fixed.items() if f}
            if fixed_nondefaults:
                node['fixed'] = fixed_nondefaults
            bounds_nondefaults = {k: b for k, b in model.bounds.items() if any(b)}
            if bounds_nondefaults:
                node['bounds'] = bounds_nondefaults

        return node

    def from_yaml_tree(self, node, tag, ctx):
        model = self.from_yaml_tree_transform(node, tag, ctx)

        if 'name' in node:
            model.name = node['name']

        if 'bounding_box' in node:
            model.bounding_box = node['bounding_box']

        param_and_model_constraints = {}
        for constraint in ['fixed', 'bounds']:
            if constraint in node:
                param_and_model_constraints[constraint] = node[constraint]
        model._initialize_constraints(param_and_model_constraints)

        yield model

        if 'inverse' in node:
            model.inverse = node['inverse']


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
