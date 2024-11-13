class UncertaintyConverter:
    tags = ("tag:astropy.org:astropy/nddata/uncertainty-*",)
    types = (
        "astropy.nddata.nduncertainty.StdDevUncertainty",
        "astropy.nddata.nduncertainty.UnknownUncertainty",
        "astropy.nddata.nduncertainty.VarianceUncertainty",
    )

    # Mapping of uncertainty class name (attribute of astropy.nddata)
    # and code "name" stored in the data file.
    # This will need to be separately versioned if the schema is updated.
    _class_name_to_code = {
        "StdDevUncertainty": "stddev",
        "UnknownUncertainty": "unknown",
        "VarianceUncertainty": "variance",
    }
    _class_code_to_name = {v: k for k, v in _class_name_to_code.items()}

    def from_yaml_tree(self, node, tag, ctx):
        import astropy.nddata

        class_name = self._class_code_to_name[node["name"]]

        return getattr(astropy.nddata, class_name)(node["array"], unit=node.get("unit"))

    def to_yaml_tree(self, obj, tag, ctx):
        node = {
            "name": self._class_name_to_code[obj.__class__.__name__],
            "array": obj.array,
        }

        if obj.unit is not None:
            node["unit"] = obj.unit

        return node
