from asdf.extension import Converter


class EarthLocationConverter(Converter):
    tags = ("tag:astropy.org:astropy/coordinates/earthlocation-*",)
    types = (
        "astropy.coordinates.earth.EarthLocation",
        "astropy.utils.masked.core.MaskedEarthLocation",
    )

    def to_yaml_tree(self, obj, tag, ctx):
        result = obj.info._represent_as_dict()
        result.pop("__class__", None)
        return result

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.coordinates.earth import EarthLocation

        return EarthLocation.info._construct_from_dict(node)
