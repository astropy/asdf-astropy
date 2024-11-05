from asdf.extension import Converter

_WCS_ATTRS = ("naxis", "colsel", "keysel", "key", "pixel_shape", "pixel_bounds")


class FitsWCSConverter(Converter):
    tags = ("tag:astropy.org:astropy/fits/fitswcs-*",)
    types = ("astropy.wcs.wcs.WCS",)

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.wcs import WCS

        if naxis := node["attrs"].pop("naxis"):
            node["hdu"][0].header["naxis"] = naxis

        pixel_shape = node["attrs"].pop("pixel_shape")
        pixel_bounds = node["attrs"].pop("pixel_bounds")

        wcs = WCS(node["hdu"][0].header, fobj=node["hdu"], **node["attrs"])

        if wcs.sip is not None:
            # work around a bug in astropy where sip headers lose precision
            wcs.sip = wcs._read_sip_kw(node["hdu"][0].header, node["attrs"].get("key", " "))
            wcs.wcs.set()

        wcs.pixel_shape = pixel_shape
        wcs.pixel_bounds = pixel_bounds
        return wcs

    def to_yaml_tree(self, wcs, tag, ctx):
        hdulist = wcs.to_fits(relax=True)
        attrs = {a: getattr(wcs, a) for a in _WCS_ATTRS if hasattr(wcs, a)}
        return {"hdu": hdulist, "attrs": attrs}
