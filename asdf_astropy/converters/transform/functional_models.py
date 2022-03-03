from packaging.version import parse as parse_version

from ..helpers import parse_tag_version
from .core import TransformConverterBase, parameter_to_value


class ConstantConverter(TransformConverterBase):
    """
    ASDF support for serializing the Const1D and Const2D models.
    """

    # The 'dimensions' property was added in 1.4.0,
    # previously all values were 1D.
    _2D_MIN_VERSION = parse_version("1.4.0")

    tags = ["tag:stsci.edu:asdf/transform/constant-*"]

    types = [
        "astropy.modeling.functional_models.Const1D",
        "astropy.modeling.functional_models.Const2D",
    ]

    def to_yaml_tree_transform(self, model, tag, ctx):
        from astropy.modeling.functional_models import Const1D, Const2D

        if parse_tag_version(tag) < self._2D_MIN_VERSION:
            if not isinstance(model, Const1D):
                raise TypeError(f"{tag} does not support models with > 1 dimension")
            return {"value": parameter_to_value(model.amplitude)}
        else:
            if isinstance(model, Const1D):
                dimension = 1
            elif isinstance(model, Const2D):
                dimension = 2
            return {"value": parameter_to_value(model.amplitude), "dimensions": dimension}

    def from_yaml_tree_transform(self, node, tag, ctx):
        from astropy.modeling.functional_models import Const1D, Const2D

        if parse_tag_version(tag) < self._2D_MIN_VERSION:
            return Const1D(node["value"])
        elif node["dimensions"] == 1:
            return Const1D(node["value"])
        elif node["dimensions"] == 2:
            return Const2D(node["value"])
