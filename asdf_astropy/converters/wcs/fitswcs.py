from asdf.extension import Converter

_WCS_ATTRS = ("naxis", "colsel", "keysel", "key", "pixel_shape", "pixel_bounds")


class FitsWCSConverter(Converter):
    tags = ("tag:astropy.org:astropy/fits/fitswcs-*",)
    types = ("astropy.wcs.wcs.WCS",)

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.wcs import WCS

        hdulist = node["hdulist"]
        attrs = node["attrs"]

        if naxis := attrs.pop("naxis"):
            hdulist[0].header["naxis"] = naxis

        pixel_shape = attrs.pop("pixel_shape")
        pixel_bounds = attrs.pop("pixel_bounds")

        wcs = WCS(hdulist[0].header, fobj=hdulist, **attrs)

        if wcs.sip is not None:
            # work around a bug in astropy where sip headers lose precision
            # see https://github.com/astropy/astropy/issues/17334
            wcs.sip = wcs._read_sip_kw(hdulist[0].header, attrs.get("key", " "))
            wcs.wcs.set()

        wcs.pixel_shape = pixel_shape
        wcs.pixel_bounds = pixel_bounds
        return wcs

    def to_yaml_tree(self, wcs, tag, ctx):
        hdulist = wcs.to_fits(relax=True)
        attrs = {a: getattr(wcs, a) for a in _WCS_ATTRS if hasattr(wcs, a)}
        return {"hdulist": hdulist, "attrs": attrs}
