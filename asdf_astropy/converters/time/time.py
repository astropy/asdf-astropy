import numpy as np
from asdf.extension import Converter
from asdf.tags.core.ndarray import NDArrayType

_GUESSABLE_FORMATS = {"iso", "byear", "jyear", "yday"}

_ASTROPY_FORMAT_TO_ASDF_FORMAT = {
    "isot": "iso",
    "byear_str": "byear",
    "jyear_str": "jyear",
}


class TimeConverter(Converter):
    tags = ("tag:stsci.edu:asdf/time/time-*",)
    types = ("astropy.time.core.Time",)

    def to_yaml_tree(self, obj, tag, ctx):
        from astropy.time import Time

        base_format = obj.format
        if base_format == "byear":
            obj = Time(obj, format="byear_str")
        elif base_format == "jyear":
            obj = Time(obj, format="jyear_str")
        elif base_format in ("fits", "datetime", "plot_date", "ymdhms", "datetime64"):
            obj = Time(obj, format="isot")

        asdf_format = _ASTROPY_FORMAT_TO_ASDF_FORMAT.get(obj.format, obj.format)
        guessable_format = asdf_format in _GUESSABLE_FORMATS

        if obj.scale == "utc" and guessable_format and obj.isscalar and base_format == obj.format:
            return obj.value

        node = {
            "value": obj.value,
        }

        if not guessable_format:
            node["format"] = asdf_format

        if base_format != obj.format:
            node["base_format"] = base_format

        if obj.scale != "utc":
            node["scale"] = obj.scale

        if obj.location is not None:
            # The 1.0.0 and 1.1.0 tags differ in how location is represented.
            # In 1.0.0, there is a single "unit" property that is shared among
            # x, y, and z, and in 1.1.0 each is a quantity with its own unit.
            location = (
                {
                    "x": obj.location.x.value,
                    "y": obj.location.y.value,
                    "z": obj.location.z.value,
                    "unit": obj.location.unit,
                }
                if tag.endswith("1.0.0")
                else {
                    "x": obj.location.x,
                    "y": obj.location.y,
                    "z": obj.location.z,
                }
            )

            node["location"] = location

        return node

    def from_yaml_tree(self, node, tag, ctx):
        from astropy import units
        from astropy.coordinates import EarthLocation
        from astropy.time import Time

        if isinstance(node, (str, list, np.ndarray, NDArrayType)):
            time = Time(node)
            asdf_format = _ASTROPY_FORMAT_TO_ASDF_FORMAT.get(time.format, time.format)
            if asdf_format not in _GUESSABLE_FORMATS:
                msg = f"ASDF time '{node}' is not one of the recognized implicit formats"
                raise ValueError(msg)

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

        time = Time(
            node["value"],
            format=node.get("format"),
            scale=node.get("scale"),
            location=location,
        )

        base_format = node.get("base_format")
        if base_format is not None and base_format != time.format:
            time.format = base_format

        return time
