from asdf_astropy.converters.helpers import get_tag_name

from .core import TransformConverterBase

__all__ = ["CompoundConverter"]


_OPERATOR_TO_TAG_NAME = {
    "+": "add",
    "-": "subtract",
    "*": "multiply",
    "/": "divide",
    "**": "power",
    "|": "compose",
    "&": "concatenate",
    "fix_inputs": "fix_inputs",
}


_TAG_NAME_TO_MODEL_METHOD = {
    "add": "__add__",
    "subtract": "__sub__",
    "multiply": "__mul__",
    "divide": "__truediv__",
    "power": "__pow__",
    "compose": "__or__",
    "concatenate": "__and__",
    "fix_inputs": "fix_inputs",
}


class CompoundConverter(TransformConverterBase):
    """
    ASDF serialization support for CompoundModel.
    """

    tags = (
        "tag:stsci.edu:asdf/transform/add-*",
        "tag:stsci.edu:asdf/transform/subtract-*",
        "tag:stsci.edu:asdf/transform/multiply-*",
        "tag:stsci.edu:asdf/transform/divide-*",
        "tag:stsci.edu:asdf/transform/power-*",
        "tag:stsci.edu:asdf/transform/compose-*",
        "tag:stsci.edu:asdf/transform/concatenate-*",
        "tag:stsci.edu:asdf/transform/fix_inputs-*",
    )
    types = ("astropy.modeling.core.CompoundModel",)

    def select_tag(self, model, tags, ctx):
        tag_name = _OPERATOR_TO_TAG_NAME[model.op]

        # The extension will never include two tags with the
        # same name but different version, so we can just
        # return the first matching tag that we discover in
        # the list:
        return next(t for t in tags if get_tag_name(t) == tag_name)

    def to_yaml_tree_transform(self, model, tag, ctx):
        left = model.left

        right = (
            {
                "keys": list(model.right.keys()),
                "values": list(model.right.values()),
            }
            if isinstance(model.right, dict)
            else model.right
        )

        return {"forward": [left, right]}

    def from_yaml_tree_transform(self, node, tag, ctx):
        from astropy.modeling.core import CompoundModel, Model

        oper = _TAG_NAME_TO_MODEL_METHOD[get_tag_name(tag)]

        left = node["forward"][0]
        if not isinstance(left, Model):
            msg = f"Unknown left model type '{node['forward'][0]._tag}'"
            raise TypeError(msg)

        right = node["forward"][1]
        if (oper == "fix_inputs" and not isinstance(right, dict)) or (
            oper != "fix_inputs" and not isinstance(right, Model)
        ):
            msg = f"Unknown right model type '{node['forward'][1]._tag}'"
            raise TypeError(msg)

        if oper == "fix_inputs":
            right = dict(zip(right["keys"], right["values"]))
            return CompoundModel("fix_inputs", left, right)

        return getattr(left, oper)(right)
