ASDF serialization support for astropy
--------------------------------------

.. image:: https://github.com/astropy/asdf-astropy/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/astropy/asdf-astropy/actions
    :alt: CI Status

.. image:: https://codecov.io/gh/astropy/asdf-astropy/branch/main/graph/badge.svg?token=0XGOYX4QGT
    :target: https://codecov.io/gh/astropy/asdf-astropy
    :alt: Code coverage

.. image:: https://github.com/astropy/asdf-astropy/workflows/Downstream/badge.svg
    :target: https://github.com/astropy/asdf-astropy/actions
    :alt: Downstream CI Status

.. image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
    :target: http://www.astropy.org
    :alt: Powered by Astropy Badge

.. image:: https://readthedocs.org/projects/asdf-astropy/badge/?version=latest
    :target: https://asdf-astropy.readthedocs.io/en/latest/

.. image:: https://zenodo.org/badge/271820376.svg
    :target: https://zenodo.org/badge/latestdoi/271820376

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit
    :alt: pre-commit

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/

This package includes plugins that provide ASDF serialization support for astropy
objects.  The plugins are automatically enabled when the package is installed.

The plugins in this package supersede those in the ``astropy.io.misc.asdf`` module;
when this package is installed, the astropy plugins will be ignored.  The
``astropy.io.misc.asdf`` module will be removed in a future version of astropy.

License
-------

This project is Copyright (c) Association of Universities for Research in Astronomy (AURA)
and licensed under the terms of the BSD 3-Clause license. This package is based upon
the `Astropy package template <https://github.com/astropy/package-template>`_
which is licensed under the BSD 3-clause license. See the licenses folder for
more information.


Installation
------------

.. _begin-pip-install-text:

Stable releases of the asdf-astropy python package are registered `at
PyPi <https://pypi.python.org/pypi/asdf-astropy>`__. The latest stable version
can be installed using ``pip``:

.. code-block:: console

    $ pip install asdf-astropy

.. _end-pip-install-text:

.. _begin-source-install-text:

The latest development version of asdf-astropy is available from the ``main`` branch
`on github <https://github.com/astropy/asdf-astropy>`__. To clone the project:

.. code-block:: console

    $ git clone https://github.com/astropy/asdf-astropy

To install:

.. code-block:: console

    $ cd asdf-astropy
    $ pip install .

To install in `development
mode <https://packaging.python.org/tutorials/distributing-packages/#working-in-development-mode>`__

.. code-block:: console

    $ pip install -e .

.. _end-source-install-text:

Testing
-------

.. _begin-testing-text:

To install the test dependencies from a source checkout of the repository:

.. code-block:: console

    $ pip install -e ".[test]"

To run the unit tests from a source checkout of the repository:

.. code-block:: console

    $ pytest

It is also possible to run the test suite from an installed version of
the package.

.. code-block:: console

    $ pip install "asdf-astropy[test]"
    $ pytest --pyargs asdf-astropy

It is also possible to run the tests using `tox
<https://tox.readthedocs.io/en/latest/>`__.

.. code-block:: console

    $ pip install tox

To list all available environments:

.. code-block:: console

    $ tox -va

To run a specific environment:

.. code-block:: console

    $ tox -e <envname>


.. _end-testing-text:


Contributing
------------

We love contributions! asdf-astropy is open source,
built on open source, and we'd love to have you hang out in our community.
