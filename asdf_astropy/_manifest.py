from itertools import chain

from asdf import extension


class CompoundManifestExtension(extension.Extension):
    """
    Combine a listed of asdf ``ManifestExtensions`` into a single extension.
    """

    def __init__(self, extensions):
        self._extensions = extensions

    @property
    def extension_uri(self):
        return self._extensions[0].extension_uri

    @property
    def asdf_standard_requirement(self):
        return self._extensions[0].asdf_standard_requirement

    @property
    def legacy_class_names(self):
        return list(chain.from_iterable(e.legacy_class_names for e in self._extensions))

    @property
    def converters(self):
        return list(chain.from_iterable(e.converters for e in self._extensions))

    @property
    def compressors(self):
        return list(chain.from_iterable(e.compressors for e in self._extensions))

    @property
    def tags(self):
        return list(chain.from_iterable(e.tags for e in self._extensions))
