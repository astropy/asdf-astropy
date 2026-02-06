from asdf.extension import Converter


class HighLevelWCSWrapperConverter(Converter):
    tags = ("tag:astropy.org:astropy/wcs/highlevelwcswrapper-*",)
    types = ("astropy.wcs.wcsapi.high_level_wcs_wrapper.HighLevelWCSWrapper",)

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.wcs.wcsapi import HighLevelWCSWrapper

        return HighLevelWCSWrapper(node["wcs"])

    def to_yaml_tree(self, hlwcs, tag, ctx):
        return {"wcs": hlwcs.low_level_wcs}
