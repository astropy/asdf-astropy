from asdf.extension import Converter


class SlicedWCSConverter(Converter):
    tags = ("tag:astropy.org:astropy/wcs/slicedwcs-*",)
    types = ("astropy.wcs.wcsapi.wrappers.sliced_wcs.SlicedLowLevelWCS",)

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS

        wcs = node["wcs"]
        slice_array = [
            s if isinstance(s, int) else slice(s["start"], s["stop"], s["step"]) for s in node["slices_array"]
        ]
        return SlicedLowLevelWCS(wcs, slice_array)

    def to_yaml_tree(self, sl, tag, ctx):
        slices_array = []

        for s in sl._slices_array:
            if isinstance(s, slice):
                slices_array.append(
                    {
                        "start": s.start,
                        "stop": s.stop,
                        "step": s.step,
                    },
                )
            else:
                slices_array.append(s)
        return {
            "wcs": sl._wcs,
            "slices_array": slices_array,
        }
