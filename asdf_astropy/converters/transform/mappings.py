from asdf.extension import Converter

from .core import TransformConverterBase


class IdentityConverter(TransformConverterBase):
    """
    ASDF support for serializing the Identity model.
    """

    tags = ("tag:stsci.edu:asdf/transform/identity-*",)
    types = ("astropy.modeling.mappings.Identity",)

    def to_yaml_tree_transform(self, model, tag, ctx):
        node = {}
        if model.n_inputs != 1:
            node["n_dims"] = model.n_inputs
        return node

    def from_yaml_tree_transform(self, node, tag, ctx):
        from astropy.modeling.mappings import Identity

        return Identity(node.get("n_dims", 1))


class RemapAxesConverter(TransformConverterBase):
    """
    ASDF support for serializing the Mapping model
    """

    tags = ("tag:stsci.edu:asdf/transform/remap_axes-*",)
    types = ("astropy.modeling.mappings.Mapping",)

    def to_yaml_tree_transform(self, model, tag, ctx):
        node = {"mapping": list(model.mapping)}
        if model.n_inputs > max(model.mapping) + 1:
            node["n_inputs"] = model.n_inputs
        return node

    def from_yaml_tree_transform(self, node, tag, ctx):
        from astropy.modeling.models import Mapping

        return Mapping(tuple(node["mapping"]), node.get("n_inputs"))


class UnitsMappingConverter(Converter):
    """
    ASDF support for serializing the UnitsMapping model.
    Note that this converter does not inherit from TransformConverterBase,
    because the inputs and outputs are written differently
    from other models.
    """

    tags = ("tag:astropy.org:astropy/transform/units_mapping-*",)
    types = ("astropy.modeling.mappings.UnitsMapping",)

    def to_yaml_tree(self, model, tag, ctx):
        node = {}

        if model.name is not None:
            node["name"] = model.name

        inputs = []
        outputs = []
        for i, o, m in zip(model.inputs, model.outputs, model.mapping):
            input_ = {
                "name": i,
                "allow_dimensionless": model.input_units_allow_dimensionless[i],
            }
            if m[0] is not None:
                input_["unit"] = m[0]
            if model.input_units_equivalencies is not None and i in model.input_units_equivalencies:
                input_["equivalencies"] = model.input_units_equivalencies[i]
            inputs.append(input_)

            output = {
                "name": o,
            }
            if m[-1] is not None:
                output["unit"] = m[-1]
            outputs.append(output)

        node["unit_inputs"] = inputs
        node["unit_outputs"] = outputs

        return node

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.modeling.mappings import UnitsMapping

        mapping = tuple((i.get("unit"), o.get("unit")) for i, o in zip(node["unit_inputs"], node["unit_outputs"]))

        equivalencies = None
        for i in node["unit_inputs"]:
            if "equivalencies" in i:
                if equivalencies is None:
                    equivalencies = {}
                equivalencies[i["name"]] = i["equivalencies"]

        kwargs = {
            "input_units_equivalencies": equivalencies,
            "input_units_allow_dimensionless": {
                i["name"]: i.get("allow_dimensionless", False) for i in node["unit_inputs"]
            },
        }

        if "name" in node:
            kwargs["name"] = node["name"]

        return UnitsMapping(mapping, **kwargs)
