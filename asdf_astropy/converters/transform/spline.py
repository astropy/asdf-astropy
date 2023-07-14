from .core import TransformConverterBase


class SplineConverter(TransformConverterBase):
    """
    ASDF support for serializing 1D spline models
    """

    tags = ("tag:stsci.edu:asdf/transform/spline1d-*",)
    types = ("astropy.modeling.spline.Spline1D",)

    def to_yaml_tree_transform(self, model, tag, ctx):
        return {"knots": model.t, "coefficients": model.c, "degree": model.degree}

    def from_yaml_tree_transform(self, node, tag, ctx):
        from astropy.modeling.spline import Spline1D

        knots = node["knots"]
        coeffs = node["coefficients"]
        degree = node["degree"]

        return Spline1D(knots, coeffs, degree)
