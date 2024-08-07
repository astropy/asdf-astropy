import ast

from asdf.extension import Converter


class SlicedWCSConverter(Converter):
    tags = ("tag:astropy.org:astropy/slicedwcs/slicedwcs-*",)
    types = ("astropy.wcs.wcsapi.wrappers.sliced_wcs.SlicedLowLevelWCS",)

    def parse_slice_string(self, slice_str):
        if slice_str.isdigit():
            return int(ast.literal_eval(slice_str))
        slice_str = slice_str[len("slice(") : -1]
        parts = slice_str.split(",")
        start = ast.literal_eval(parts[0].strip())
        stop = ast.literal_eval(parts[1].strip())
        step = ast.literal_eval(parts[2].strip())
        return slice(start, stop, step)

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS

        wcs = node["wcs"]
        slice_array = node["slices_array"]
        slice_array = [self.parse_slice_string(s) for s in slice_array]

        return SlicedLowLevelWCS(wcs, slice_array)

    def to_yaml_tree(self, sl, tag, ctx):
        import astropy

        node = {}
        if isinstance(sl._wcs, astropy.wcs.WCS):
            node["wcs"] = sl._wcs
        node["slices_array"] = [str(item) for item in sl._slices_array]
        return node
