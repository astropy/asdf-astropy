import importlib


def import_type(type_name):
    """
    Import a Python type from its fully-qualified name.
    For example, when this method is called with 'builtins.str'
    it will return the `str` type.

    Parameters
    ----------
    type_name : str
        Type name, with module.

    Returns
    -------
    type
    """
    module_name, class_name = type_name.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)


# FIXME: ASTROPY_LT_7_1: Remove once we depend on astropy >= 7.1.
def import_masked_type(class_name):
    try:
        return import_type(f"astropy.utils.masked.core.Masked{class_name}")
    except AttributeError as e:
        from astropy import __version__
        from packaging.version import Version

        if Version(__version__) < Version("7.1.dev"):
            msg = (
                f"ASDF support for masked {class_name} objects requires "
                f"Astropy 7.1 or newer, but you have {__version__}"
            )
            raise NotImplementedError(msg) from e
        raise
