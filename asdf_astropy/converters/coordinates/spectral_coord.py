from asdf.extension import Converter
from asdf.tags.core.ndarray import NDArrayType


class SpectralCoordConverter(Converter):
    tags = ("tag:astropy.org:astropy/coordinates/spectralcoord-*",)
    types = ("astropy.coordinates.spectral_coordinate.SpectralCoord",)

    def to_yaml_tree(self, obj, tag, ctx):
        node = {
            "value": obj.value,
            "unit": obj.unit,
        }

        if obj.observer is not None:
            node["observer"] = obj.observer

        if obj.target is not None:
            node["target"] = obj.target

        return node

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.coordinates.spectral_coordinate import SpectralCoord

        value = node["value"]
        if isinstance(value, NDArrayType):
            # TODO: Why doesn't NDArrayType work?  This needs some research
            # and documentation.  See similar note in QuantityConverter.
            value = value._make_array()

        return SpectralCoord(
            value,
            unit=node["unit"],
            observer=node.get("observer"),
            target=node.get("target"),
        )
