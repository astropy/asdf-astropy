from asdf.extension import Converter
from asdf.tags.core.ndarray import NDArrayType


class ColumnConverter(Converter):
    tags = ["tag:stsci.edu:asdf/core/column-*"]

    types = [
        "astropy.table.column.Column",
        "astropy.table.column.MaskedColumn",
    ]

    def to_yaml_tree(self, obj, tag, ctx):
        node = {
            "data": obj.data,
            "name": obj.name
        }

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

        if isinstance(data, MaskedArray):
            column_class = MaskedColumn
        else:
            column_class = Column

        return column_class(
            data=data,
            name=node["name"],
            description=node.get("description"),
            unit=node.get("unit"),
            meta=node.get("meta"),
        )


class AsdfTableConverter(Converter):
    tags = ["tag:stsci.edu:asdf/core/table-*"]

    types = []

    def to_yaml_tree(self, obj, tag, ctx):
        raise NotImplementedError("astropy does not support writing astropy.table.Table with the ASDF table-1.0.0 tag")

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.table import Table

        return Table(node["columns"], meta=node["meta"])


class AstropyTableConverter(Converter):
    tags = ["tag:astropy.org:astropy/table/table-*"]

    types = [
        "astropy.table.table.Table",
        "astropy.table.table.QTable",
    ]

    def to_yaml_tree(self, obj, tag, ctx):
        from astropy.table import QTable

        node = {
            "columns": [obj[name] for name in obj.colnames],
            "colnames": obj.colnames,
            "qtable": isinstance(obj, QTable)
        }

        if obj.meta:
            node["meta"] = obj.meta

        return node

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.table import Table, QTable

        if node.get("qtable", False):
            table = QTable(meta=node.get("meta"))
        else:
            table = Table(meta=node.get("meta"))

        for name, column in zip(node["colnames"], node["columns"]):
            table[name] = column

        return table
