from asdf.extension import Converter
from asdf.tags.core.ndarray import NDArrayType


class QuantityConverter(Converter):
    tags = ("tag:stsci.edu:asdf/unit/quantity-*",)
    types = (
        "astropy.units.quantity.Quantity",
        # The Distance class has no tag of its own, so we
        # just serialize it as a quantity.
        "astropy.coordinates.distances.Distance",
        "astropy.utils.masked.core.MaskedQuantity",
    )

    def to_yaml_tree(self, obj, tag, ctx):
        import numpy as np
        from astropy.utils.masked import Masked

        node = {
            "value": np.ma.asarray(obj.value) if isinstance(obj, Masked) else obj.value,
            "unit": obj.unit,
        }

        if obj.isscalar:
            node["datatype"] = obj.dtype.name

        return node

    def from_yaml_tree(self, node, tag, ctx):
        # numpy 2.0 changed behavior for copy where an error is produced
        # if False and a copy is required (previously there was no error)
        # astropy 6.1 changed Quantity in a similar way
        import numpy as np
        from astropy.units import Quantity

        copy = None if np.lib.NumpyVersion(np.__version__) >= "2.0.0b1" else False

        value = node["value"]
        dtype = node.get("datatype", None)
        if isinstance(value, NDArrayType):
            # TODO: Why doesn't NDArrayType work?  This needs some research
            # and documentation.
            value = value._make_array()
            dtype = value.dtype

        if isinstance(value, np.ma.MaskedArray):
            from astropy.utils import minversion
            from astropy.utils.masked import Masked

            if not minversion("astropy", "7.1.dev"):  # ASTROPY_GE_7_1
                msg = "MaskedQuantity support requires astropy 7.1 or later"
                raise NotImplementedError(msg)
            class_ = Masked(Quantity)
        else:
            class_ = Quantity

        return class_(value, unit=node["unit"], copy=copy, dtype=dtype)
