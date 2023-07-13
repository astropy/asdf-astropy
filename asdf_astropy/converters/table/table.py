from asdf.extension import Converter
from asdf.tags.core.ndarray import NDArrayType


class ColumnConverter(Converter):
    @property
    def tags(self):
        return ["tag:stsci.edu:asdf/core/column-*"]

    @property
    def types(self):
        return [
            "astropy.table.column.Column",
            "astropy.table.column.MaskedColumn",
        ]

    def to_yaml_tree(self, obj, tag, ctx):
        node = {"data": obj.data, "name": obj.name}

        if obj.description:
            node["description"] = obj.description

        if obj.unit:
            node["unit"] = obj.unit

        if obj.meta:
            node["meta"] = obj.meta

        return node

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.table import Column, MaskedColumn
        from numpy.ma.core import MaskedArray

        data = node["data"]
        if isinstance(data, NDArrayType):
            # TODO: Why doesn't NDArrayType work?  This needs some research
            # and documentation.
            data = data._make_array()

        column_class = MaskedColumn if isinstance(data, MaskedArray) else Column

        return column_class(
            data=data,
            name=node["name"],
            description=node.get("description"),
            unit=node.get("unit"),
            meta=node.get("meta"),
        )


class AsdfTableConverter(Converter):
    @property
    def tags(self):
        return ["tag:stsci.edu:asdf/core/table-*"]

    @property
    def types(self):
        return []

    def to_yaml_tree(self, obj, tag, ctx):
        msg = "astropy does not support writing astropy.table.Table with the ASDF table-1.0.0 tag"
        raise NotImplementedError(msg)

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.table import Table

        return Table(node["columns"], meta=node.get("meta"))


class AstropyTableConverter(Converter):
    @property
    def tags(self):
        return ["tag:astropy.org:astropy/table/table-*"]

    @property
    def types(self):
        return [
            "astropy.table.table.Table",
            "astropy.table.table.QTable",
        ]

    def to_yaml_tree(self, obj, tag, ctx):
        from astropy.table import QTable

        node = {
            "columns": [obj[name] for name in obj.colnames],
            "colnames": obj.colnames,
            "qtable": isinstance(obj, QTable),
        }

        if obj.meta:
            node["meta"] = obj.meta

        return node

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.table import QTable, Table

        table = QTable(meta=node.get("meta")) if node.get("qtable", False) else Table(meta=node.get("meta"))

        for name, column in zip(node["colnames"], node["columns"]):
            table[name] = column

        return table
