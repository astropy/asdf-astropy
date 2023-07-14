from asdf.extension import Converter

from asdf_astropy.converters.utils import import_type


class FrameConverter(Converter):
    def __init__(self, tags, frame_type_name):
        self._frame_type_name = frame_type_name
        self._frame_type = None

        if isinstance(tags, str):
            tags = [tags]
        self._tags = tags

    @property
    def tags(self):
        return self._tags

    @property
    def types(self):
        return [self._frame_type_name]

    @property
    def frame_type(self):
        # Delay import until the frame class is needed to improve speed
        # of loading the extension.
        if self._frame_type is None:
            self._frame_type = import_type(self._frame_type_name)
        return self._frame_type

    def to_yaml_tree(self, obj, tag, ctx):
        node = {}

        if obj.has_data:
            node["data"] = obj.data

        # TODO: Figure out why we can't use the frame_attributes
        # values and document.
        frame_attributes = {}
        for attr in obj.frame_attributes:
            value = getattr(obj, attr, None)
            if value is not None:
                frame_attributes[attr] = value
        node["frame_attributes"] = frame_attributes

        return node

    def from_yaml_tree(self, node, tag, ctx):
        data = node.get("data", None)
        if data is not None:
            return self.frame_type(node["data"], **node["frame_attributes"])

        return self.frame_type(**node["frame_attributes"])


class LegacyICRSConverter(Converter):
    tags = ("tag:astropy.org:astropy/coordinates/frames/icrs-1.0.0",)
    # Leave the types list empty so that the 1.1.0 ICRS converter
    # is used on write.
    types = ()

    def to_yaml_tree(self, obj, tag, ctx):
        from astropy.units import Quantity

        return {
            "ra": {
                "value": obj.ra.value,
                "unit": obj.ra.unit.to_string(),
                "wrap_angle": Quantity(obj.ra.wrap_angle),
            },
            "dec": {
                "value": obj.dec.value,
                "unit": obj.dec.unit.to_string(),
            },
        }

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.coordinates import ICRS, Angle, Latitude, Longitude

        ra = Longitude(node["ra"]["value"], unit=node["ra"]["unit"], wrap_angle=Angle(node["ra"]["wrap_angle"]))

        dec = Latitude(node["dec"]["value"], unit=node["dec"]["unit"])

        return ICRS(ra=ra, dec=dec)
