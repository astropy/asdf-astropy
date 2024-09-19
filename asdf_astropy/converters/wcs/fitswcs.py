from asdf.extension import Converter


class FitsWCSConverter(Converter):
    tags = ("tag:astropy.org:astropy/fits/fitswcs-*",)
    types = ("astropy.wcs.wcs.WCS",)

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.wcs import WCS

        return WCS(node["hdu"][0].header, fobj=node["hdu"])

    def to_yaml_tree(self, wcs, tag, ctx):
        node = {}
        if wcs.sip is not None:
            node["hdu"] = wcs.to_fits(relax=True)
        else:
            node["hdu"] = wcs.to_fits()
        return node
