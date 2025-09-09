from asdf.extension import Converter

from asdf_astropy.exceptions import InconsistentWCSError

# These attributes don't end up in the hdulist and
# instead will be stored in "attrs"
_WCS_ATTRS = ("naxis", "colsel", "keysel", "key", "pixel_bounds", "pixel_shape")


class WCSConverter(Converter):
    tags = ("tag:astropy.org:astropy/wcs/wcs-*",)
    types = ("astropy.wcs.wcs.WCS",)

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.wcs import WCS

        hdulist = node["hdulist"]
        attrs = node["attrs"]

        if naxis := attrs.pop("naxis"):
            hdulist[0].header["naxis"] = naxis

        # pop attrs that are not valid kwargs
        pixel_shape = attrs.pop("pixel_shape")
        pixel_bounds = attrs.pop("pixel_bounds")

        wcs = WCS(hdulist[0].header, fobj=hdulist, **attrs)

        wcs.pixel_shape = pixel_shape
        wcs.pixel_bounds = pixel_bounds

        if wcs.sip is not None:
            # work around a bug in astropy where sip headers lose precision
            # see https://github.com/astropy/astropy/issues/17334
            wcs.sip = wcs._read_sip_kw(hdulist[0].header, attrs.get("key", " "))
            wcs.wcs.set()

        return wcs

    def to_yaml_tree(self, wcs, tag, ctx):
        # Check that wcs is consistent. Astropy inconsistently checks
        # that certain expected attributes match. We need to check this
        # here to prevent writing inconsistent files that would be problematic
        # to open.
        if naxis := wcs.naxis:
            for attr in ("pixel_shape", "pixel_bounds"):
                if value := getattr(wcs, attr):
                    if len(value) != naxis:
                        msg = f"{attr} shape ({len(value)}) does not match naxis ({naxis})"
                        raise InconsistentWCSError(msg)
        hdulist = wcs.to_fits(relax=True)
        attrs = {a: getattr(wcs, a) for a in _WCS_ATTRS if hasattr(wcs, a)}
        return {"hdulist": hdulist, "attrs": attrs}
