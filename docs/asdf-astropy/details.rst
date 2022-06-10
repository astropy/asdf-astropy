.. _details:

=======
Details
=======

**ASDF** makes use of an abstract data type definition called a **tag**, which is a formed
from a **schema** or collection of **schemas**. Each **schema** encodes part of the
information that **ASDF** uses to both validate and identify the organization and types of
data within an ASDF file. Tags are assigned to specific a specific schema or collection
of schemas within a **manifest**. Finally, **ASDF** requires **converter** classes which implement
the logic of serializing and deserializing of objects (in this case **astropy** classes) into
and out of their respective **ASDF** tag representations.

The **asdf-astropy** package primarily defines **converters** for many **astropy**
types, and then properly registers them with **ASDF**. Users should never need to refer
to converter implementations directly. Their presence should be entirely transparent
when processing ASDF files.

The converters in **asdf-astropy** related to transforms implement the tags that are
defined by the :ref:`asdf-transform-schemas package <asdf-transform-schemas:asdf-transform-schemas>`.
Similarly, the converters in **asdf-astropy** related to coordinates implement
the tags that are defined by the
:ref:`asdf-coordinates-schemas package <asdf-coordinates-schemas:asdf-coordinates-schemas>`.
Moreover, many of the converters in **asdf-astropy** related to units implement tags
that are defined in the :ref:`ASDF-standard <asdf-standard:asdf-standard>`.
Finally, there are converters in **asdf-astropy** whose tags are defined within **asdf-astropy**
itself. See :ref:`asdf-astropy_manifest` for a listing of all these tags. Documentation of the
individual schemas defined by **asdf-astropy**, which are used to assemble these tags can be
found in :ref:`asdf-astropy_schemas`.

.. note::
    Not all **astropy** types are currently serializable by ASDF. Attempting to
    write unsupported types to an ASDF file will lead to a ``RepresenterError``. In
    order to support new types, new tags and converters must be created. A basic
    example can be found in :ref:`basic_example`, for additional details please refer to
    :ref:`asdf:extending_extensions`.
    If you do write additional converters or schemas please consider contributing them to **asdf-astropy**.
