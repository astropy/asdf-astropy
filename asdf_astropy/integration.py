import sys

from asdf.resource import DirectoryResourceMapping

if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources


def get_resource_mappings():
    """
    Get the resource mapping instances for the astropy schemas
    and manifests.  This method is registered with the
    asdf.resource_mappings entry point.

    Returns
    -------
    list of collections.abc.Mapping
    """
    from . import resources

    resources_root = importlib_resources.files(resources)

    return [
        DirectoryResourceMapping(resources_root / "schemas", "http://astropy.org/schemas/astropy/", recursive=True),
        DirectoryResourceMapping(resources_root / "manifests", "asdf://astropy.org/astropy/manifests/"),
    ]


def get_extensions():
    """
    Get the extension instances for the various astropy
    extensions.  This method is registered with the
    asdf.extensions entry point.

    Returns
    -------
    list of asdf.extension.Extension
    """
    from . import extensions

    return [
        extensions.ASTROPY_EXTENSION,
        extensions.COORDINATES_EXTENSION,
        *extensions.TRANSFORM_EXTENSIONS,
        *extensions.CORE_EXTENSIONS,
    ]
