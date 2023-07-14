from asdf.extension import Converter


class MagUnitConverter(Converter):
    tags = ("tag:astropy.org:astropy/units/magunit-*",)
    types = ("astropy.units.function.logarithmic.MagUnit",)

    def to_yaml_tree(self, obj, tag, ctx):
        return {"unit": obj.physical_unit}

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.units import mag

        return mag(node["unit"])
