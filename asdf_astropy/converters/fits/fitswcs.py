from asdf.extension import Converter


class FitsWCSConverter(Converter):
    tags = ("tag:astropy.org:astropy/fits/fitswcs-*",)
    types = ("astropy.wcs.wcs.WCS",)

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.wcs import WCS

        primary_hdu = node["hdu"][0]
        return WCS(primary_hdu.header)

    def to_yaml_tree(self, wcs, tag, ctx):
        node = {}
        node["hdu"] = wcs.to_fits()
        return node
