from asdf.extension import Converter


class SkyCoordConverter(Converter):
    @property
    def tags(self):
        return ["tag:astropy.org:astropy/coordinates/skycoord-*"]

    @property
    def types(self):
        return ["astropy.coordinates.sky_coordinate.SkyCoord"]

    def to_yaml_tree(self, obj, tag, ctx):
        return obj.info._represent_as_dict()

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.coordinates.sky_coordinate import SkyCoord

        return SkyCoord.info._construct_from_dict(node)
