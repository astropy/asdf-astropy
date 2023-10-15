from asdf.extension import Converter
from asdf.tags.core.ndarray import NDArrayType
from asdf.tagged import TaggedDict


class ColumnConverter(Converter):
    tags = ("tag:stsci.edu:asdf/core/column-*",)
    types = (
        "astropy.table.column.Column",
        "astropy.table.column.MaskedColumn",
    )

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
    tags = (
        "tag:stsci.edu:asdf/core/table-1.0.0",
        "tag:stsci.edu:asdf/core/table-1.1.0",
    )
    types = (
        "astropy.table.table.Table",
        "astropy.table.table.QTable",
    )

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.table import Table

        return Table(node["columns"], meta=node.get("meta"))

    def to_yaml_tree(self, obj, tag, ctx):
        from astropy.table import Column, QTable, Table

        if isinstance(obj, QTable):
            obj = Table(obj)

        for column in obj.columns.values():
            if not isinstance(column, Column):
                msg = f"The ASDF table converter does not support columns of type '{type(column)}'";
                raise NotImplementedError(msg)

        node = {
            "columns": [c for c in obj.columns.values()]
        }

        if obj.meta:
            node["meta"] = obj.meta

        return node


class AsdfTableConverterReadOnly(AsdfTableConverter):
    types = ()

    def to_yaml_tree(self, obj, tag, ctx):
        msg = (
            "The default configuration of asdf-astropy does not support writing "
            f"astropy.table.Table with the {tag} tag.  "
            "Call asdf_astropy.configure_core_table_support(asdf.get_config()) to use the ASDF core table tags."
        )
        raise NotImplementedError(msg)


class AstropyTableConverter(Converter):
    tags = ("tag:astropy.org:astropy/table/table-*",)
    types = (
        "astropy.table.table.Table",
        "astropy.table.table.QTable",
    )

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


class NdarrayMixinConverter(Converter):
    tags = ("tag:astropy.org:astropy/table/ndarraymixin-*",)
    types = ("astropy.table.ndarray_mixin.NdarrayMixin",)

    def to_yaml_tree(self, obj, tag, ctx):
        import numpy as np

        return {"array": np.asarray(obj)}

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.table import NdarrayMixin

        arr = node["array"]

        # this will trigger reading the ASDF block that contains the array data
        return arr.view(NdarrayMixin)
