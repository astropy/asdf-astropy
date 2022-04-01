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


# NOTE: ignored is only supported by astropy develop (v5.1+), not astropy LTS (v5.0.x)
class CompoundBoundingBoxConverter(Converter):
    tags = ["tag:stsci.edu:asdf/transform/property/compound_bounding_box-1.0.0"]
    types = ["astropy.modeling.bounding_box.CompoundBoundingBox"]

    def to_yaml_tree(self, cbbox, tag, ctx):
        return {
            "selector_args": [{"argument": sa.name(cbbox._model), "ignore": sa.ignore} for sa in cbbox.selector_args],
            "cbbox": [{"key": list(key), "bbox": bbox} for key, bbox in cbbox.bounding_boxes.items()],
            "ignore": cbbox.ignored_inputs,
            "order": cbbox.order,
        }

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.modeling.bounding_box import CompoundBoundingBox

        selector_args = tuple([(selector["argument"], selector["ignore"]) for selector in node["selector_args"]])
        bboxes = {tuple(bbox["key"]): bbox["bbox"] for bbox in node["cbbox"]}

        if "ignore" in node:
            ignored = node["ignore"]
        else:
            ignored = None

        if "order" in node:
            order = node["order"]
        else:
            order = "C"

        def create_bounding_box(model):
            bounding_boxes = {key: bbox(model) for key, bbox in bboxes.items()}

            return CompoundBoundingBox(bounding_boxes, model, selector_args, ignored=ignored, order=order)

        return create_bounding_box
