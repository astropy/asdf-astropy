# This file connects ASDF to the astropy.table.Table class
import contextlib

import asdf
from astropy.io import registry as io_registry
from astropy.table import Table


def read_table(filename, data_key=None, find_table=None, **kwargs):
    """
    Read a `~astropy.table.Table` object from an ASDF file

    By default, this function will look for a Table object with the key of
    ``data`` in the top-level ASDF tree. The parameters ``data_key`` and
    ``find_key`` can be used to override the default behavior.

    This function is registered as the Table reader for ASDF files with the
    unified I/O interface.

    Parameters
    ----------
    filename : str or :class:`py.path:local`
        Name of the file to be read
    data_key : str
        Optional top-level key to use for finding the Table in the tree. If not
        provided, uses ``data`` by default. Use of this parameter is not
        compatible with ``find_table``.
    find_table : function
        Optional function to be used for locating the Table in the tree. The
        function takes a single parameter, which is a dictionary representing
        the top of the ASDF tree. The function must return a
        `~astropy.table.Table` instance.

    Returns
    -------
    table : `~astropy.table.Table`
        `~astropy.table.Table` instance
    """
    if data_key and find_table:
        msg = "Options 'data_key' and 'find_table' are not compatible"
        raise ValueError(msg)

    with asdf.open(filename, **kwargs) as af:
        if find_table:
            return find_table(af.tree)

        return af[data_key or "data"]


def write_table(table, filename, data_key=None, make_tree=None, **kwargs):
    """
    Write a `~astropy.table.Table` object to an ASDF file.

    By default, this function will write a Table object in the top-level ASDF
    tree using the key of ``data``. The parameters ``data_key`` and
    ``make_tree`` can be used to override the default behavior.

    This function is registered as the Table writer for ASDF files with the
    unified I/O interface.

    Parameters
    ----------
    table : `~astropy.table.Table`
        `~astropy.table.Table` instance to be written
    filename : str or :class:`py.path:local`
        Name of the new ASDF file to be created
    data_key : str
        Optional top-level key in the ASDF tree to use when writing the Table.
        If not provided, uses ``data`` by default. Use of this parameter is not
        compatible with ``make_tree``.
    make_tree : function
        Optional function to be used for creating the ASDF tree. The function
        takes a single parameter, which is the `~astropy.table.Table` instance
        to be written. The function must return a `dict` representing the ASDF
        tree to be created.
    """
    if data_key and make_tree:
        msg = "Options 'data_key' and 'make_tree' are not compatible"
        raise ValueError(msg)

    tree = make_tree(table) if make_tree else {data_key or "data": table}

    with asdf.AsdfFile(tree) as af:
        af.write_to(filename, **kwargs)


def asdf_identify(origin, filepath, fileobj, *args, **kwargs):
    return filepath is not None and filepath.endswith(".asdf")


# This means we're using an older version of astropy
# and it has already claimed the 'asdf' identifier.
with contextlib.suppress(io_registry.IORegistryError):
    io_registry.register_reader("asdf", Table, read_table)
    io_registry.register_writer("asdf", Table, write_table)
    io_registry.register_identifier("asdf", Table, asdf_identify)
