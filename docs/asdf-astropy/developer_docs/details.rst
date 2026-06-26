.. _details:

=======
Details
=======

**ASDF** provides an :ref:`extension API <asdf:extending_extensions>` that **asdf-astropy**
uses to support reading and writing **astropy** objects. The details here should be of
no concern to users since the process of converting **astropy** objects to **ASDF**
is transparent, the user need only provide the **astropy** object or **ASDF** file
and the rest will be handled for them.

Developers and maintainers may want to know more about how **asdf-astropy** works
and should start by referring to the :ref:`asdf extension API documentation <asdf:extending_extensions>`.
In brief, **asdf-astropy** implements **extensions** that provide mappings between
**tags** that get written to or read from **ASDF** files, are associated with **schemas**
to check that data is handles properly and **converter** classes that handle the logic
of reading and writing.

The converters in **asdf-astropy** related to transforms correspond to schemas
defined by the :ref:`asdf-transform-schemas package <asdf-transform-schemas:asdf-transform-schemas>`.
Similarly, the converters in **asdf-astropy** related to coordinates correspond to
schemas defined in the
:ref:`asdf-coordinates-schemas package <asdf-coordinates-schemas:asdf-coordinates-schemas>`.
Moreover, many of the converters in **asdf-astropy** related to units correspond to schemas
that are defined in the :ref:`ASDF astronomy schemas <asdf-standard:astronomy-schema>`.
Finally, there are converters in **asdf-astropy** that correspond to schemas within **asdf-astropy**
itself. See the respective packages for schema details and :ref:`asdf-astropy_manifest`
and :ref:`asdf-astropy_schemas` for resources defined within this package.

.. note::
    Not all **astropy** types are currently serializable by ASDF. Attempting to
    write unsupported types to an ASDF file will lead to a ``RepresenterError``. In
    order to support new types, new tags and converters must be created. A basic
    example can be found in :ref:`basic_example`, for additional details please refer to
    :ref:`asdf:extending_extensions`.
    If you do write additional converters or schemas please consider contributing them to **asdf-astropy**.
