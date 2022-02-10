from asdf.extension import Converter

from ..utils import import_type


class CosmologyConverter(Converter):

    def __init__(self, tag, cosmology_type_name):
        self._tag = tag
        self._cosmology_type_name = cosmology_type_name
        self._cosmology_type = None

    @property
    def tags(self):
        return [self._tag]

    @property
    def types(self):
        return [self._cosmology_type_name]

    @property
    def cosmology_type(self):
        # Delay import until the cosmology class is needed to improve speed
        # of loading the extension.
        if self._cosmology_type is None:
            self._cosmology_type = import_type(self._cosmology_type_name)
        return self._cosmology_type

    def to_yaml_tree(self, obj, tag, ctx):
        return obj.to_format("mapping")

    def from_yaml_tree(self, node, tag, ctx):
        return self.cosmology_type.from_format(node, format="mapping")
