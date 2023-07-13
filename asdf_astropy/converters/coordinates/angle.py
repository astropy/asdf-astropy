from asdf_astropy.converters.unit.quantity import QuantityConverter


class AngleConverter(QuantityConverter):
    @property
    def tags(self):
        return ["tag:astropy.org:astropy/coordinates/angle-*"]

    @property
    def types(self):
        return ["astropy.coordinates.angles.Angle"]

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.coordinates.angles import Angle

        return Angle(super().from_yaml_tree(node, tag, ctx))


class LatitudeConverter(QuantityConverter):
    @property
    def tags(self):
        return ["tag:astropy.org:astropy/coordinates/latitude-*"]

    @property
    def types(self):
        return ["astropy.coordinates.angles.Latitude"]

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.coordinates.angles import Latitude

        return Latitude(super().from_yaml_tree(node, tag, ctx))


class LongitudeConverter(QuantityConverter):
    @property
    def tags(self):
        return ["tag:astropy.org:astropy/coordinates/longitude-*"]

    @property
    def types(self):
        return ["astropy.coordinates.angles.Longitude"]

    def to_yaml_tree(self, obj, tag, ctx):
        tree = super().to_yaml_tree(obj, tag, ctx)
        tree["wrap_angle"] = obj.wrap_angle
        return tree

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.coordinates.angles import Longitude

        return Longitude(super().from_yaml_tree(node, tag, ctx), wrap_angle=node["wrap_angle"])
