import importlib.resources as importlib_resources

from asdf.resource import DirectoryResourceMapping


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
        *extensions.ASTROPY_EXTENSIONS,
        *extensions.COORDINATES_EXTENSIONS,
        *extensions.TRANSFORM_EXTENSIONS,
        *extensions.UNIT_EXTENSIONS,
        *extensions.CORE_EXTENSIONS,
        *extensions.EMPTY_EXTENSIONS,
    ]
