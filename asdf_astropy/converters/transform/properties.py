from asdf.extension import Converter


class ModelBoundingBoxConverter(Converter):
    tags = ("tag:stsci.edu:asdf/transform/property/bounding_box-*",)
    types = ("astropy.modeling.bounding_box.ModelBoundingBox",)

    def to_yaml_tree(self, bbox, tag, ctx):
        return {
            "intervals": {_input: list(interval) for _input, interval in bbox.named_intervals.items()},
            "ignore": list(bbox.ignored_inputs),
            "order": bbox.order,
        }

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.modeling.bounding_box import ModelBoundingBox, get_index, get_name

        intervals = {_input: tuple(interval) for _input, interval in node["intervals"].items()}

        ignored = node["ignore"] if "ignore" in node else []

        order = node["order"] if "order" in node else "C"

        def create_bounding_box(model, cbbox=None):
            if cbbox is None:
                ignore = ignored
            else:
                # Hack to pass compound_bounding_box selector_args ignore in 5.0.4+
                ignore = list(
                    set(ignored + [get_name(model, get_index(model, key)) for key in cbbox.selector_args.ignore]),
                )
                # Add in globally ignored inputs from the compound_bounding_box in 5.1+
                ignore = list(set(ignore + [get_name(model, get_index(model, key)) for key in cbbox.ignored]))

            return ModelBoundingBox(intervals, model, ignored=ignore, order=order)

        return create_bounding_box


class CompoundBoundingBoxConverter(Converter):
    tags = ("tag:stsci.edu:asdf/transform/property/compound_bounding_box-*",)
    types = ("astropy.modeling.bounding_box.CompoundBoundingBox",)

    def to_yaml_tree(self, cbbox, tag, ctx):
        node = {
            "selector_args": [{"argument": sa.name(cbbox._model), "ignore": sa.ignore} for sa in cbbox.selector_args],
            "cbbox": [{"key": list(key), "bbox": bbox} for key, bbox in cbbox.bounding_boxes.items()],
            "order": cbbox.order,
        }

        node["ignore"] = cbbox.ignored_inputs

        return node

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.modeling.bounding_box import CompoundBoundingBox

        selector_args = tuple((selector["argument"], selector["ignore"]) for selector in node["selector_args"])
        bboxes = {tuple(bbox["key"]): bbox["bbox"] for bbox in node["cbbox"]}

        ignored = node["ignore"] if "ignore" in node else []

        order = node["order"] if "order" in node else "C"

        def create_bounding_box(model):
            cbbox = CompoundBoundingBox({}, model, selector_args, ignored=ignored, order=order)

            for key, bb in bboxes.items():
                cbbox[key] = bb(model, cbbox)

            return cbbox

        return create_bounding_box
