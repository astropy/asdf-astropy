from asdf.extension import Converter

from asdf_astropy.converters.utils import import_type


class FrameConverter(Converter):
    def __init__(self, tags, frame_type_name):
        self._frame_type_name = frame_type_name
        self._frame_type = None

        if isinstance(tags, str):
            tags = [tags]
        self._tags = tags

    def select_tag(self, obj, tags, ctx):
        # Implement select_tag since coordinates-1.0.0 has 2 icrs tags
        # When writing use latest (only impacts icrs-1.0.0/1.1.0)
        return sorted(tags)[-1]

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
        if tag == "tag:astropy.org:astropy/coordinates/frames/icrs-1.0.0":
            # icrs-1.0.0 is special cased since it's schema/representation is odd
            from astropy.coordinates import ICRS, Angle, Latitude, Longitude

            ra = Longitude(node["ra"]["value"], unit=node["ra"]["unit"], wrap_angle=Angle(node["ra"]["wrap_angle"]))
            dec = Latitude(node["dec"]["value"], unit=node["dec"]["unit"])
            return ICRS(ra=ra, dec=dec)

        data = node.get("data", None)
        if data is not None:
            return self.frame_type(node["data"], **node["frame_attributes"])

        return self.frame_type(**node["frame_attributes"])
