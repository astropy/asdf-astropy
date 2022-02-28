ASDF serialization support for astropy
--------------------------------------

.. image:: https://github.com/astropy/asdf-astropy/workflows/CI/badge.svg
    :target: https://github.com/astropy/asdf-astropy/actions
    :alt: CI Status

.. image:: https://codecov.io/gh/astropy/asdf-astropy/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/astropy/asdf-astropy/branch=main
    :alt: Code coverage

.. image:: https://github.com/astropy/asdf-astropy/workflows/Downstream/badge.svg
    :target: https://github.com/astropy/asdf-astropy/actions
    :alt: Downstream CI Status

.. image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
    :target: http://www.astropy.org
    :alt: Powered by Astropy Badge

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit
    :alt: pre-commit

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/

This package includes plugins that provide ASDF serialization support for astropy
objects.  The plugins are automatically enabled when the package is installed.

The plugins in this package supercede those in the ``astropy.io.misc.asdf`` module;
when this package is installed, the astropy plugins will be ignored.  The
``astropy.io.misc.asdf`` module will be removed in a future version of astropy.

License
-------

This project is Copyright (c) Association of Universities for Research in Astronomy (AURA)
and licensed under the terms of the BSD 3-Clause license. This package is based upon
the `Astropy package template <https://github.com/astropy/package-template>`_
which is licensed under the BSD 3-clause license. See the licenses folder for
more information.


Contributing
------------

We love contributions! asdf-astropy is open source,
built on open source, and we'd love to have you hang out in our community.
