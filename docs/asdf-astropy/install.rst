.. _installation:

************
Installation
************

There are several different ways to install the `asdf-astropy` package.
Each is described in detail below.

Requirements
============

The `asdf-astropy` package has several dependencies which are all listed
in the project's ``setup.cfg`` file. All dependencies are available on
pypi and will be automatically installed along with `asdf-astropy`.
Most importantly, both the `asdf` and `astropy` packages will be installed
along with `asdf-astropy` which should enable full functionality.

Installation with pip
=====================

.. include:: ../../README.rst
    :start-after: begin-pip-install-text:
    :end-before: end-pip-install-text:

Installing with conda
=====================

`asdf-astropy` is also distributed as a `conda <https://conda.io/docs/>`__
package via the `conda-forge <https://conda-forge.org/>`__ channel.

To install `asdf-astropy` within an existing conda environment

.. code-block:: console

    $ conda install -c conda-forge asdf-astropy

To create a new conda environment and install `asdf-astropy`

.. code-block:: console

    $ conda create -n new-env-name -c conda-forge python asdf-astropy

Building from source
====================

.. include:: ../../README.rst
    :start-after: begin-source-install-text:
    :end-before: end-source-install-text:

Running the tests
=================

.. include:: ../../README.rst
    :start-after: begin-testing-text:
    :end-before: end-testing-text:
