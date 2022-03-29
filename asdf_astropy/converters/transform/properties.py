from asdf.extension import Converter


class ModelBoundingBoxConverter(Converter):
    tags = ["tag:stsci.edu:asdf/transform/property/bounding_box-1.0.0"]
    types = ["astropy.modeling.bounding_box.ModelBoundingBox"]

    def to_yaml_tree(self, bbox, tag, ctx):
        return {
            "intervals": {_input: list(interval) for _input, interval in bbox.intervals.items()},
            "ignore": list(bbox.ignored),
            "order": bbox.order,
        }

    def from_yaml_tree(self, node, tag, ctx):
        intervals = {_input: tuple(interval) for _input, interval in node["intervals"].items()}

        if "ignore" in node:
            ignored = node["ignore"]
        else:
            ignored = None

        if "order" in node:
            order = node["order"]
        else:
            order = "C"

        return intervals, ignored, order
