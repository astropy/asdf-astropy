from asdf.extension import Converter


class EarthLocationConverter(Converter):
    @property
    def tags(self):
        return ["tag:astropy.org:astropy/coordinates/earthlocation-*"]

    @property
    def types(self):
        return ["astropy.coordinates.earth.EarthLocation"]

    def to_yaml_tree(self, obj, tag, ctx):
        return obj.info._represent_as_dict()

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.coordinates.earth import EarthLocation

        return EarthLocation.info._construct_from_dict(node)
