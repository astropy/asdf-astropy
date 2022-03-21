.. _details:

=======
Details
=======

The `asdf-astropy` package defines classes, referred to as **converters**, that
implement the logic for serialization and deserialization of ``astropy`` types.
Users should never need to refer to converter implementations directly. Their
presence should be entirely transparent when processing ASDF files.

ASDF makes use of abstract data type definitions called `schemas`, which typically
have an associated `tag`. ASDF uses tags in order to identify the different
types of data within an ASDF file in order to know how to read or write it.
The converter classes provided here are specific implementations of particular `tags`.

The converters in ``asdf-astropy`` related to transforms implement the
tags and schemas that are defined by the
`asdf-transform-schemas <https://github.com/asdf-format/asdf-transform-schemas>`_.
Similarly, the converters in ``asdf-astropy`` related to coordinates implement
the tags and schemas that are defined by the
`asdf-coordinates-schemas <https://github.com/asdf-format/asdf-coordinates-schemas>`_.
In other cases, both the converters and tags/schemas are defined within ``asdf-astropy`` itself.
Documentation of the individual schemas defined by
``asdf-astropy`` can be found in
:ref:`asdf-astropy_schemas`.

Not all ``astropy`` types are currently serializable by ASDF. Attempting to
write unsupported types to an ASDF file will lead to a ``RepresenterError``. In
order to support new types, new converters and schemas must be created. See `Writing
ASDF Extensions <https://asdf.readthedocs.io/en/latest/asdf/extending/extensions.html>`_
for additional details, as well as the following example. If you do write additional
converters or schemas please consider contributing them to ``asdf-astropy``.
