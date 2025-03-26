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
