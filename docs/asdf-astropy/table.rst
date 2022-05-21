.. _table:

*****************************
Using **ASDF** with Table I/O
*****************************

**ASDF** provides readers and writers for `~astropy.table.Table` using the
:ref:`table_io`. This makes it convenient to read and write **ASDF** files with
`~astropy.table.Table` data.

Basic Usage
===========

Given a table, it is possible to write it out to an **ASDF** file::

    from astropy.table import Table

    # Create a simple table
    t = Table(dtype=[('a', 'f4'), ('b', 'i4'), ('c', 'S2')])
    # Write the table to an ASDF file
    t.write('table.asdf')

The I/O registry automatically selects the appropriate writer function to use
based on the ``.asdf`` extension of the output file.

Reading a file generated in this way is also possible using
`~astropy.table.Table.read`::

    t2 = Table.read('table.asdf')

The I/O registry automatically selects the appropriate reader function based on
the extension of the input file.

In the case of both reading and writing, if the file extension is not ``.asdf``
it is possible to explicitly specify the reader/writer function to be used::

    t3 = Table.read('table.zxcv', format='asdf')

Advanced Usage
^^^^^^^^^^^^^^

The fundamental **ASDF** data structure is the tree, which is a nested
combination of basic data structures (see :ref:`asdf:data-model` for a more
detailed description). At the top level, the tree is a `dict`.

The consequence of this is that a `~astropy.table.Table` object (or any object,
for that matter) can be stored at any arbitrary location within an **ASDF** tree.
The basic writer use case described above stores the given
`~astropy.table.Table` at the top of the tree using a default key. The basic
reader case assumes that a `~astropy.table.Table` is stored in the same place.

However, it may sometimes be useful for users to specify a different top-level
key to be used for storage and retrieval of a `~astropy.table.Table` from an
**ASDF** file. For this reason, the **ASDF** I/O interface provides ``data_key`` as an
optional keyword when writing and reading::

    from astropy.table import Table

    t = Table(dtype=[('a', 'f4'), ('b', 'i4'), ('c', 'S2')])
    # Write the table to an asdf file using a non-default key
    t.write('foo.asdf', data_key='foo')

A `~astropy.table.Table` stored using a custom data key can be retrieved by
passing the same argument to `~astropy.table.Table.read`::

    foo = Table.read('foo.asdf', data_key='foo')

The ``data_key`` option only applies to `~astropy.table.Table` objects that are
stored at the top of the **ASDF** tree. For full generality, users may pass a
callback when writing or reading **ASDF** files to define precisely where the
`~astropy.table.Table` object should be placed in the tree. The option for the
write case is ``make_tree``. The function callback should accept exactly one
argument, which is the `~astropy.table.Table` object, and should return a
`dict` representing the tree to be stored::

    def make_custom_tree(table):
        # Return a nested tree where the table is stored at the second level
        return dict(foo=dict(bar=table))

    t = Table(dtype=[('a', 'f4'), ('b', 'i4'), ('c', 'S2')])
    # Write the table to an **ASDF** file using a non-default key
    t.write('foobar.asdf', make_tree=make_custom_tree)

Similarly, when reading an **ASDF** file, the user can pass a custom callback to
locate the table within the **ASDF** tree. The option in this case is
``find_table``. The callback should accept exactly one argument, which is an
`dict` representing the **ASDF** tree, and it should return a
`~astropy.table.Table` object::

    def find_table(tree):
        # This returns the Table that was stored by the example above
        return tree['foo']['bar']

    foo = Table.read('foobar.asdf', find_table=find_table)
