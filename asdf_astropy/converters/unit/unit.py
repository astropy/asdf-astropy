from asdf.extension import Converter


class UnitConverter(Converter):
    tags = (
        "tag:stsci.edu:asdf/unit/unit-*",
        "tag:astropy.org:astropy/units/unit-*",
    )
    types = (
        "astropy.units.core.CompositeUnit",
        "astropy.units.core.IrreducibleUnit",
        "astropy.units.core.NamedUnit",
        "astropy.units.core.PrefixUnit",
        "astropy.units.core.Unit",
        "astropy.units.core.UnitBase",
        "astropy.units.core.UnrecognizedUnit",
        "astropy.units.function.mixin.IrreducibleFunctionUnit",
        "astropy.units.function.mixin.RegularFunctionUnit",
    )

    def select_tag(self, obj, tags, ctx):
        return next(t for t in tags if "astropy.org" in t)

    def to_yaml_tree(self, obj, tag, ctx):
        return obj.to_string()

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.units import Unit

        kwargs = {"parse_strict": "silent"}
        if "stsci.edu" in tag:
            kwargs["format"] = "vounit"

        return Unit(node, **kwargs)
