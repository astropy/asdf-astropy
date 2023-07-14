from .core import TransformConverterBase

__all__ = ["TabularConverter"]


class TabularConverter(TransformConverterBase):
    """
    ASDF support for serializing tabular models.
    """

    tags = ("tag:stsci.edu:asdf/transform/tabular-*",)
    types = (
        "astropy.modeling.tabular.Tabular1D",
        "astropy.modeling.tabular.Tabular2D",
    )

    def to_yaml_tree_transform(self, model, tag, ctx):
        node = {}
        if model.fill_value is not None:
            node["fill_value"] = model.fill_value
        node["lookup_table"] = model.lookup_table
        node["points"] = list(model.points)
        node["method"] = str(model.method)
        node["bounds_error"] = model.bounds_error

        return node

    def from_yaml_tree_transform(self, node, tag, ctx):
        from astropy.modeling import tabular

        lookup_table = node.pop("lookup_table")
        dim = lookup_table.ndim
        fill_value = node.pop("fill_value", None)
        if dim == 1:
            points = (node["points"][0],)
            model = tabular.Tabular1D(
                points=points,
                lookup_table=lookup_table,
                method=node["method"],
                bounds_error=node["bounds_error"],
                fill_value=fill_value,
            )
        elif dim == 2:  # noqa: PLR2004
            points = tuple(node["points"])
            model = tabular.Tabular2D(
                points=points,
                lookup_table=lookup_table,
                method=node["method"],
                bounds_error=node["bounds_error"],
                fill_value=fill_value,
            )
        else:
            msg = "tabular models with ndim > 2 are not supported "
            raise NotImplementedError(msg)

        return model
