from asdf.extension import Converter
from asdf.tags.core.ndarray import NDArrayType


class QuantityConverter(Converter):
    tags = ["tag:stsci.edu:asdf/unit/quantity-*"]

    types = [
        "astropy.units.quantity.Quantity",
        # The Distance class has no tag of its own, so we
        # just serialize it as a quantity.
        "astropy.coordinates.distances.Distance",
    ]

    def to_yaml_tree(self, obj, tag, ctx):
        node = {
            "value": obj.value,
            "unit": obj.unit,
        }

        if obj.isscalar:
            node["datatype"] = obj.dtype.name

        return node

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.units import Quantity

        value = node["value"]
        dtype = node.get("datatype", None)
        if isinstance(value, NDArrayType):
            # TODO: Why doesn't NDArrayType work?  This needs some research
            # and documentation.
            value = value._make_array()
            dtype = value.dtype

        return Quantity(value, unit=node["unit"], copy=False, dtype=dtype)
