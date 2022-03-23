.. _asdf-astropy_schemas:


====================
asdf-astropy Schemas
====================

Documentation for each of the individual ASDF schemas defined by **asdf-astropy** can
be found at the links below.

Documentation for the schemas defined in the ASDF Standard can be found `here
<https://asdf-standard.readthedocs.io/en/latest/schemas/index.html>`__.
Note that other schemas are defined in
`asdf-transform-schemas <https://github.com/asdf-format/asdf-transform-schemas>`_
and
`asdf-coordinates-schemas <https://github.com/asdf-format/asdf-coordinates-schemas>`_.


.. contents::

FITS
----

The following schemas are associated with ``astropy`` types from the
:ref:`astropy-io-fits` submodule:

fits/fits-1.0.0
^^^^^^^^^^^^^^^

.. literalinclude:: ../../asdf_astropy/resources/schemas/fits/fits-1.0.0.yaml
   :language: yaml


Table
-----

The following schemas are associated with ``astropy`` types from the
:ref:`astropy-table` submodule:

table/table-1.0.0
^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../asdf_astropy/resources/schemas/table/table-1.0.0.yaml
   :language: yaml


Time
----

The following schemas are associated with ``astropy`` types from the
:ref:`astropy-time` submodule:

time/timedelta-1.0.0
^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../asdf_astropy/resources/schemas/time/timedelta-1.0.0.yaml
   :language: yaml


Units
-----

The following schemas are associated with ``astropy`` types from the
:ref:`astropy-units` submodule:

units/equivalency-1.0.0
^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../asdf_astropy/resources/schemas/units/equivalency-1.0.0.yaml
   :language: yaml
