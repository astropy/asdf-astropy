from asdf.extension import Converter


class FitsWCSConverter(Converter):
    """
    Converter for serializing and deserializing `astropy.wcs.WCS` objects.

    This converter currently supports the serialization of simple WCS objects
    by preserving the `wcs.to_header()` data. It does not support complex WCS objects
    such as tabular or distortion WCSes.

    Future work:
        - Until the support for tabular and distortion WCSes is added,
          throw error for such WCSes when passed through in the converter
        - Implement mechanisms to detect tabular and distortion WCSes and support their serialization
    """

    tags = ("tag:astropy.org:astropy/fits/fitswcs-*",)
    types = ("astropy.wcs.wcs.WCS",)

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.wcs import WCS

        header = node["header"]
        return WCS(header)

    def to_yaml_tree(self, wcs, tag, ctx):
        node = {}
        node["header"] = dict(wcs.to_header())
        return node
