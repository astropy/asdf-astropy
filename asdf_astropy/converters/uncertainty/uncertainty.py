from asdf.extension import Converter


class UncertaintyConverter(Converter):
    tags = ("tag:astropy.org:astropy/uncertainty/uncertainty-*",)
    types = ("astropy.nddata.nduncertainty.Uncertainty",)

    def from_yaml_tree(self, node, tag, ctx):
        return (node["array"], node.get("unit"))

    def to_yaml_tree(self, nddata_uncertainty, tag, ctx):
        node = {}

        node["array"] = nddata_uncertainty.array
        if nddata_uncertainty.unit is not None:
            node["unit"] = nddata_uncertainty.unit

        return node


class StdDevUncertaintyConverter(UncertaintyConverter):
    tags = ("tag:astropy.org:astropy/uncertainty/stddevuncertainty-*",)
    types = ("astropy.nddata.nduncertainty.StdDevUncertainty",)

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.nddata import StdDevUncertainty

        array, unit = super().from_yaml_tree(node, tag, ctx)
        return StdDevUncertainty(array=array, unit=unit)


class UnknownUncertaintyConverter(UncertaintyConverter):
    tags = ("tag:astropy.org:astropy/uncertainty/unknownuncertainty-*",)
    types = ("astropy.nddata.nduncertainty.UnknownUncertainty",)

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.nddata import UnknownUncertainty

        array, unit = super().from_yaml_tree(node, tag, ctx)
        return UnknownUncertainty(array=array, unit=unit)
