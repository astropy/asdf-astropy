from asdf.versioning import split_tag_version

from .unit import UnitConverter


class MagUnitConverter(UnitConverter):
    tags = ("tag:astropy.org:astropy/units/magunit-*",)
    types = ("astropy.units.function.logarithmic.MagUnit",)

    def select_tag(self, obj, tags, ctx):
        return tags[-1]

    def to_yaml_tree(self, obj, tag, ctx):
        _, version = split_tag_version(tag)

        # version 1.0.0 uses a nested dictionary
        if version == "1.0.0":
            return {"unit": obj.physical_unit}

        return super().to_yaml_tree(obj.physical_unit, tag, ctx)

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.units import mag

        _, version = split_tag_version(tag)

        # version 1.0.0 uses a nested dictionary
        if version == "1.0.0":
            return mag(node["unit"])

        return mag(super().from_yaml_tree(node, tag, ctx))
