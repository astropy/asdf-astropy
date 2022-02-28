from asdf.extension import Converter


class UnitConverter(Converter):
    tags = ["tag:stsci.edu:asdf/unit/unit-*"]

    types = [
        "astropy.units.core.CompositeUnit",
        "astropy.units.core.IrreducibleUnit",
        "astropy.units.core.NamedUnit",
        "astropy.units.core.PrefixUnit",
        "astropy.units.core.Unit",
        "astropy.units.core.UnitBase",
        "astropy.units.core.UnrecognizedUnit",
        "astropy.units.function.mixin.IrreducibleFunctionUnit",
        "astropy.units.function.mixin.RegularFunctionUnit",
    ]

    def to_yaml_tree(self, obj, tag, ctx):
        from astropy.units import UnitsError

        try:
            return obj.to_string(format="vounit")
        except (UnitsError, ValueError) as e:
            raise ValueError(f"Unit '{obj}' is not representable as VOUnit and cannot be serialized to ASDF") from e

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.units import Unit

        return Unit(node, format="vounit", parse_strict="silent")
