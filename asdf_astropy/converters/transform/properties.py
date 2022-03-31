from asdf.extension import Converter


class ModelBoundingBoxConverter(Converter):
    tags = ["tag:stsci.edu:asdf/transform/property/bounding_box-1.0.0"]
    types = ["astropy.modeling.bounding_box.ModelBoundingBox"]

    def to_yaml_tree(self, bbox, tag, ctx):
        return {
            "intervals": {_input: list(interval) for _input, interval in bbox.named_intervals.items()},
            "ignore": list(bbox.ignored_inputs),
            "order": bbox.order,
        }

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.modeling.bounding_box import ModelBoundingBox

        intervals = {_input: tuple(interval) for _input, interval in node["intervals"].items()}

        if "ignore" in node:
            ignored = node["ignore"]
        else:
            ignored = None

        if "order" in node:
            order = node["order"]
        else:
            order = "C"

        def create_bounding_box(model):
            return ModelBoundingBox(intervals, model, ignored=ignored, order=order)

        return create_bounding_box
