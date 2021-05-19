from asdf.extension import Converter
from asdf.tags.core.ndarray import NDArrayType
import numpy as np


_GUESSABLE_FORMATS = {"iso", "byear", "jyear", "yday"}

_ASTROPY_FORMAT_TO_ASDF_FORMAT = {
    "isot": "iso",
    "byear_str": "byear",
    "jyear_str": "jyear",
}


class TimeConverter(Converter):
    tags = ["tag:stsci.edu:asdf/time/time-*"]

    types = ["astropy.time.core.Time"]

    def to_yaml_tree(self, obj, tag, ctx):
        from astropy.time import Time

        if obj.format == "byear":
            obj = Time(obj, format="byear_str")
        elif obj.format == "jyear":
            obj = Time(obj, format="jyear_str")
        elif obj.format in ("fits", "datetime", "plot_date"):
            obj = Time(obj, format="isot")

        asdf_format = _ASTROPY_FORMAT_TO_ASDF_FORMAT.get(obj.format, obj.format)
        guessable_format = asdf_format in _GUESSABLE_FORMATS

        if obj.scale == "utc" and guessable_format and obj.isscalar:
            return obj.value

        node = {
            "value": obj.value,
        }

        if not guessable_format:
            node["format"] = asdf_format

        if obj.scale != "utc":
            node["scale"] = obj.scale

        if obj.location is not None:
            # The 1.0.0 and 1.1.0 tags differ in how location is represented.
            # In 1.0.0, there is a single "unit" property that is shared among
            # x, y, and z, and in 1.1.0 each is a quantity with its own unit.
            if tag.endswith("1.0.0"):
                location = {
                    "x": obj.location.x.value,
                    "y": obj.location.y.value,
                    "z": obj.location.z.value,
                    "unit": obj.location.unit,
                }
            else:
                location = {
                    "x": obj.location.x,
                    "y": obj.location.y,
                    "z": obj.location.z,
                }

            node["location"] = location

        return node

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.time import Time
        from astropy import units
        from astropy.coordinates import EarthLocation

        if isinstance(node, (str, list, np.ndarray, NDArrayType)):
            time = Time(node)
            asdf_format = _ASTROPY_FORMAT_TO_ASDF_FORMAT.get(time.format, time.format)
            if asdf_format not in _GUESSABLE_FORMATS:
                raise ValueError(f"ASDF time '{node}' is not one of the recognized implicit formats")

            return time

        location = node.get("location")
        if location is not None:
            # The 1.0.0 and 1.1.0 tags differ in how location is represented.
            # In 1.0.0, there is a single "unit" property that is shared among
            # x, y, and z, and in 1.1.0 each is a quantity with its own unit.
            if tag.endswith("1.0.0"):
                unit = location.get("unit", units.m)
                location = EarthLocation.from_geocentric(
                    units.Quantity(location["x"], unit=unit),
                    units.Quantity(location["y"], unit=unit),
                    units.Quantity(location["z"], unit=unit),
                )
            else:
                location = EarthLocation.from_geocentric(
                    location["x"],
                    location["y"],
                    location["z"],
                )

        return Time(
            node["value"],
            format=node.get("format"),
            scale=node.get("scale"),
            location=location,
        )
