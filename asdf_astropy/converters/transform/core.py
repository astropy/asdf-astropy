import abc
import warnings

import numpy as np
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
                node['fixed'] = fixed_nondefaults
            bounds_nondefaults = {k: b for k, b in model.bounds.items() if any(b)}
            if bounds_nondefaults:
                node['bounds'] = bounds_nondefaults

        return node

    def _serialize_bounding_box(self, model, node):
        from packaging.version import Version
        import astropy

        if Version(astropy.__version__) > Version('4.999.999'):
            self._serialize_bounding_box_astropy_5(model, node)
        else:
            self._serialize_bounding_box_astropy_4(model, node)

    def _serialize_bounding_box_astropy_4(self, model, node):
        try:
            bb = model.bounding_box
        except NotImplementedError:
            bb = None

        if bb is not None:
            if model.n_inputs == 1:
                bb = list(bb)
            else:
                bb = [list(item) for item in model.bounding_box]
            node['bounding_box'] = bb

    def _serialize_bounding_box_astropy_5(self, model, node):
        from astropy.modeling.bounding_box import ModelBoundingBox, CompoundBoundingBox

        try:
            bb = model.bounding_box
        except NotImplementedError:
            bb = None

        if isinstance(bb, ModelBoundingBox):
            bb = bb.bounding_box(order='C')

            if model.n_inputs == 1:
                bb = list(bb)
            else:
                bb = [list(item) for item in bb]
            node['bounding_box'] = bb

        elif isinstance(bb, CompoundBoundingBox):
            selector_args = [[sa.index, sa.ignore] for sa in bb.selector_args]
            node['selector_args'] = selector_args
            node['cbbox_keys'] = list(bb.bounding_boxes.keys())

            bounding_boxes = list(bb.bounding_boxes.values())
            if len(model.inputs) - len(selector_args) == 1:
                node['cbbox_values'] = [list(sbbox.bounding_box()) for sbbox in bounding_boxes]
            else:
                node['cbbox_values'] = [[list(item) for item in sbbox.bounding_box()
                                         if np.isfinite(item[0])] for sbbox in bounding_boxes]

    def from_yaml_tree(self, node, tag, ctx):
        model = self.from_yaml_tree_transform(node, tag, ctx)

        if 'name' in node:
            model.name = node['name']

        self._deserialize_bounding_box(model, node)

        if 'inputs' in node:
            model.inputs = tuple(node['inputs'])

        if 'outputs' in node:
            model.outputs = tuple(node['outputs'])

        param_and_model_constraints = {}
        for constraint in ['fixed', 'bounds']:
            if constraint in node:
                param_and_model_constraints[constraint] = node[constraint]
        model._initialize_constraints(param_and_model_constraints)

        yield model

        if 'inverse' in node:
            model.inverse = node['inverse']

    def _deserialize_bounding_box(self, model, node):
        from packaging.version import Version
        import astropy

        if Version(astropy.__version__) > Version('4.999.999'):
            self._deserialize_bounding_box_astropy_5(model, node)
        else:
            self._deserialize_bounding_box_astropy_4(model, node)

    def _deserialize_bounding_box_astropy_4(self, model, node):
        if 'bounding_box' in node:
            model.bounding_box = node['bounding_box']
        elif 'selector_args' in node:
            warnings.warn("This version of astropy does not support compound bounding boxes.")

    def _deserialize_bounding_box_astropy_5(self, model, node):
        from astropy.modeling.bounding_box import CompoundBoundingBox

        if 'bounding_box' in node:
            model.bounding_box = node['bounding_box']
        elif 'selector_args' in node:
            cbbox_keys = [tuple(key) for key in node['cbbox_keys']]
            bbox_dict = dict(zip(cbbox_keys, node['cbbox_values']))

            selector_args = node['selector_args']
            model.bounding_box = CompoundBoundingBox.validate(model, bbox_dict, selector_args)


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
