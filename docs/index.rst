.. _asdf-astropy:

**************************************
The **asdf-astropy** Extension Package
**************************************

The **asdf-astropy** package contains code that is used to serialize **astropy**
objects so that they can be represented and stored using the Advanced Scientific
Data Format (**ASDF**).

If **asdf-astropy** is installed, no further configuration is required in order
to process **ASDF** files that contain **astropy** objects. Note that the **ASDF**
package has been designed to automatically detect the presence of tags defined by
packages like **asdf-astropy** and automatically make use of that package's support
infrastructure to operate correctly.

Documentation on the **ASDF Standard** can be found :ref:`here <asdf-standard:asdf-standard>`.
Documentation on the **ASDF** Python library can be found :ref:`here <asdf:asdf>`.


Getting Started
===============

.. toctree::
    :maxdepth: 2

    asdf-astropy/install.rst
    asdf-astropy/quickstart.rst
    asdf-astropy/migrating.rst

Using **asdf-astropy**
======================

.. toctree::
    :maxdepth: 2

    asdf-astropy/table.rst
    asdf-astropy/details.rst
    asdf-astropy/example.rst
    asdf-astropy/manifest.rst
    asdf-astropy/schemas.rst
    asdf-astropy/api.rst
