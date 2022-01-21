from asdf.extension import Converter


class ModelBoundingBoxConverter(Converter):
    tags = ["tag:stsci.edu:asdf/transform/property/bounding_box-1.0.0"]
    types = ["astropy.modeling.bounding_box.ModelBoundingBox"]

    def to_yaml_tree(self, bbox, tag, ctx):
        from astropy.modeling.bounding_box import ModelBoundingBox

        if isinstance(bbox, ModelBoundingBox):
            return {
                'intervals': {
                    _input: list(interval) for _input, interval in bbox.intervals.items()
                },
                'ignore': list(bbox.ignored),
                'order': bbox.order
            }
        else:
            raise TypeError(f"{bbox} is not a valid ModelBoundingBox!")

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.modeling.bounding_box import ModelBoundingBox

        intervals = {
            _input: tuple(interval) for _input, interval in node['intervals'].items()
        }

        if 'ignore' in node:
            ignored = node['ignore']
        else:
            ignored = None

        if 'order' in node:
            order = node['order']
        else:
            order = 'C'

        return ModelBoundingBox(intervals, ignored=ignored, order=order)


class CompoundBoundingBoxConverter(Converter):
    tags = ["tag:stsci.edu:asdf/transform/property/compound_bounding_box-1.0.0"]
    types = ["astropy.modeling.bounding_box.CompoundBoundingBox"]

    def to_yaml_tree(self, cbbox, tag, ctx):
        from astropy.modeling.bounding_box import CompoundBoundingBox

        if isinstance(cbbox, CompoundBoundingBox):
            return {
                'selector_args': [
                    {
                        'argument': sa[0],
                        'ignore': sa[1]
                    } for sa in cbbox.selector_args
                ],
                'cbbox': [
                    {
                        'key': list(key),
                        'bbox': bbox
                    } for key, bbox in cbbox.bounding_boxes.items()
                ],
                'ignore': cbbox.global_ignored,
                'order': cbbox.order
            }
        else:
            raise TypeError(f"{cbbox} is not a valid CompoundBoundingBox!")

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.modeling.bounding_box import CompoundBoundingBox

        selector_args = tuple([
            (selector['argument'], selector['ignore']) for selector in node['selector_args']
        ])

        bounding_boxes = {
            tuple(bbox['key']): bbox['bbox']
            for bbox in node['cbbox']
        }

        if 'ignore' in node:
            ignored = node['ignore']
        else:
            ignored = None

        if 'order' in node:
            order = node['order']
        else:
            order = 'C'

        return CompoundBoundingBox(bounding_boxes, selector_args=selector_args, ignored=ignored, order=order)
