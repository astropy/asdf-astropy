from .core import TransformConverterBase, import_type, parameter_to_value


class ProjectionConverter(TransformConverterBase):
    """
    ASDF support for serializing most projection models.
    An instance of this class must be created for each
    projection.

    Parameters
    ----------
    tags : list of str
        Tag patterns.
    pix2sky_type_name : str
        Fully-qualified type name of the projection's Pix2Sky model.
    sky2pix_type_name : str
        Fully-qualified type name of the projection's Sky2Pix model.
    """

    def __init__(self, tags, pix2sky_type_name, sky2pix_type_name):
        self._tags = tags
        self._pix2sky_type_name = pix2sky_type_name
        self._sky2pix_type_name = sky2pix_type_name
        self._pix2sky_type = None
        self._sky2pix_type = None

    @property
    def tags(self):
        return self._tags

    @property
    def types(self):
        return [self._pix2sky_type_name, self._sky2pix_type_name]

    @property
    def pix2sky_type(self):
        # Delay import until the model class is needed to improve speed
        # of loading the extension.
        if self._pix2sky_type is None:
            self._pix2sky_type = import_type(self._pix2sky_type_name)
        return self._pix2sky_type

    @property
    def sky2pix_type(self):
        # Delay import until the model class is needed to improve speed
        # of loading the extension.
        if self._sky2pix_type is None:
            self._sky2pix_type = import_type(self._sky2pix_type_name)
        return self._sky2pix_type

    def to_yaml_tree_transform(self, model, tag, ctx):
        if isinstance(model, self.pix2sky_type):
            direction = "pix2sky"
        elif isinstance(model, self.sky2pix_type):
            direction = "sky2pix"
        else:
            msg = f"Unrecognized projection model type: {type(model)}"
            raise TypeError(msg)

        node = {p: parameter_to_value(getattr(model, p)) for p in model.param_names}
        node["direction"] = direction

        return node

    def from_yaml_tree_transform(self, node, tag, ctx):
        if node["direction"] == "pix2sky":
            model_type = self.pix2sky_type
        elif node["direction"] == "sky2pix":
            model_type = self.sky2pix_type
        else:
            msg = f"Unrecognized projection direction: {node['direction']}"
            raise ValueError(msg)

        model_kwargs = {}
        for param in model_type.param_names:
            if param in node:
                model_kwargs[param] = node[param]
        return model_type(**model_kwargs)
