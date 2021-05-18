from asdf.extension import Converter
from asdf.tags.core.ndarray import NDArrayType


class QuantityConverter(Converter):
    tags = ["tag:stsci.edu:asdf/unit/quantity-*"]

    types = ["astropy.units.quantity.Quantity"]

    def to_yaml_tree(self, obj, tag, ctx):
        return {
            "value": obj.value,
            "unit": obj.unit,
        }

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.units import Quantity

        value = node["value"]
        if isinstance(value, NDArrayType):
            # TODO: Why doesn't NDArrayType work?  This needs some research
            # and documentation.
            value = value._make_array()

        return Quantity(value, unit=node["unit"])
