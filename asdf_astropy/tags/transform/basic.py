# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

from asdf.versioning import AsdfVersion
import asdf

from astropy.modeling import models
from astropy.modeling.core import CompoundModel

from . import _parameter_to_value


__all__ = ['TransformConverter', 'IdentityConverter', 'ConstantConverter']


class TransformConverter(asdf.AsdfConverter):

    def _from_tree_base_transform_members(self, model, node):
        if 'name' in node:
            model.name = node['name']

        if 'bounding_box' in node:
            model.bounding_box = node['bounding_box']

        if "inputs" in node:
            if model.n_inputs == 1:
                model.inputs = (node["inputs"],)
            else:
                model.inputs = tuple(node["inputs"])

        if "outputs" in node:
            if model.n_outputs == 1:
                model.outputs = (node["outputs"],)
            else:
                model.outputs = tuple(node["outputs"])

        param_and_model_constraints = {}
        for constraint in ['fixed', 'bounds']:
            if constraint in node:
                param_and_model_constraints[constraint] = node[constraint]

        yield model
        model._initialize_constraints(param_and_model_constraints)
        if 'inverse' in node:
            model.inverse = node['inverse']

    def from_tree_transform(self, node):
        raise NotImplementedError(
            "Must be implemented in TransformConverter subclasses")

    def from_yaml_tree(self, node):
        model = self.from_tree_transform(node)
        return self._from_tree_base_transform_members(model, node)

    def _to_tree_base_transform_members(self, model, node):
        if getattr(model, '_user_inverse', None) is not None:
            node['inverse'] = model._user_inverse

        if model.name is not None:
            node['name'] = model.name

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
        if type(model.__class__.inputs) != property:
            node['inputs'] = model.inputs
            node['outputs'] = model.outputs

        # model / parameter constraints
        if not isinstance(model, CompoundModel):
            fixed_nondefaults = {k: f for k, f in model.fixed.items() if f}
            if fixed_nondefaults:
                node['fixed'] = fixed_nondefaults
            bounds_nondefaults = {k: b for k, b in model.bounds.items() if any(b)}
            if bounds_nondefaults:
                node['bounds'] = bounds_nondefaults

        return node

    def to_tree_transform(self, model):
        raise NotImplementedError("Must be implemented in TransformConverter subclasses")

    def to_yaml_tree(self, model):
        node = self.to_tree_transform(model)
        return self._to_tree_base_transform_members(model, node)

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        assert a.name == b.name
        # TODO: Assert inverses are the same


class IdentityConverter(TransformConverter):
    tags = {"http://asdf-format.org/schemas/transform/identity-2.0.0",
            "tag:stsci.edu:asdf/transform/identity-1.0.0",
            "tag:stsci.edu:asdf/transform/identity-1.1.0",
            "tag:stsci.edu:asdf/transform/identity-1.2.0",
            }

    types = {models.Identity}

    def from_tree_transform(self, node):
        return models.Identity(node.get('n_dims', 1))

    def to_tree_transform(self, model):
        node = {}
        if model.n_inputs != 1:
            node['n_dims'] = model.n_inputs
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, models.Identity) and
                isinstance(b, models.Identity) and
                a.n_inputs == b.n_inputs)


class ConstantConverter(TransformConverter):
    tags = {"http://asdf-format.org/schemas/transform/constant-2.0.0",
            "tag:stsci.edu:asdf/transform/constant-1.0.0",
            "tag:stsci.edu:asdf/transform/constant-1.1.0",
            "tag:stsci.edu:asdf/transform/constant-1.2.0",
            "tag:stsci.edu:asdf/transform/constant-1.3.0",
            "tag:stsci.edu:asdf/transform/constant-1.4.0",
            }
    types = {models.Const1D, models.Const2D}

    def from_tree_transform(self, node):
        if self.version < AsdfVersion('1.4.0'):
            # The 'dimensions' property was added in 1.4.0,
            # previously all values were 1D.
            return models.Const1D(node['value'])
        elif node['dimensions'] == 1:
            return models.Const1D(node['value'])
        elif node['dimensions'] == 2:
            return models.Const2D(node['value'])

    def to_tree_transform(self, model):
        if self.version < AsdfVersion('1.4.0'):
            if not isinstance(model, models.Const1D):
                raise ValueError(
                    f'constant-{self.version} does not support models with > 1 dimension')
            return {
                'value': _parameter_to_value(model.amplitude)
            }
        else:
            if isinstance(model, models.Const1D):
                dimension = 1
            elif isinstance(model, models.Const2D):
                dimension = 2
            return {
                'value': _parameter_to_value(model.amplitude),
                'dimensions': dimension
            }


class UnitsMappingConverter(asdf.AsdfConverter):
    tags = {"http://asdf-format.org/schemas/transform/units_mapping-2.0.0",
            "tag:astropy.org:astropy/transform/units_mapping-1.0.0"
            }
    types = {models.UnitsMapping}

    def to_tree_transform(self, model):
        tree = {}

        if model.name is not None:
            tree["name"] = model.name

        inputs = []
        outputs = []
        for i, o, m in zip(model.inputs, model.outputs, model.mapping):
            input = {
                "name": i,
                "allow_dimensionless": model.input_units_allow_dimensionless[i],
            }
            if m[0] is not None:
                input["unit"] = m[0]
            if model.input_units_equivalencies is not None and i in model.input_units_equivalencies:
                input["equivalencies"] = model.input_units_equivalencies[i]
            inputs.append(input)

            output = {
                "name": o,
            }
            if m[-1] is not None:
                output["unit"] = m[-1]
            outputs.append(output)

        tree["inputs"] = inputs
        tree["outputs"] = outputs

        return tree

    def from_tree_transform(self, node):
        mapping = tuple((i.get("unit"), o.get("unit"))
                        for i, o in zip(node["inputs"], node["outputs"]))

        equivalencies = None
        for i in node["inputs"]:
            if "equivalencies" in i:
                if equivalencies is None:
                    equivalencies = {}
                equivalencies[i["name"]] = i["equivalencies"]

        kwargs = {
            "input_units_equivalencies": equivalencies,
            "input_units_allow_dimensionless": {
                i["name"]: i.get("allow_dimensionless", False) for i in node["inputs"]},
        }

        if "name" in node:
            kwargs["name"] = node["name"]

        return models.UnitsMapping(mapping, **kwargs)
