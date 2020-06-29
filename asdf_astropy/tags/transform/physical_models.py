# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

from numpy.testing import assert_array_equal


from astropy.modeling import physical_models
from .basic import TransformConverter
from . import _parameter_to_value


__all__ = ['BlackBody', 'Drude1DConverter', 'Plummer1DConverter']


class BlackBody(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/blackbody-2.0.0",
            "tag:stsci.edu:asdf/transform/blackbody-1.0.0",
            }

    types = {physical_models.BlackBody}

    def from_tree_transform(self, node):
        return physical_models.BlackBody(scale=node['scale'],
                                         temperature=node['temperature'])

    def to_tree_transform(self, model):
        node = {'scale': _parameter_to_value(model.scale),
                'temperature': _parameter_to_value(model.temperature)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, physical_models.BlackBody) and
                isinstance(b, physical_models.BlackBody))
        assert_array_equal(a.scale, b.scale)
        assert_array_equal(a.temperature, b.temperature)


class Drude1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/drude1d-2.0.0",
            "tag:stsci.edu:asdf/transform/drude1d-1.0.0",
            }

    types = {physical_models.Drude1D}

    def from_tree_transform(self, node):
        return physical_models.Drude1D(amplitude=node['amplitude'],
                                       x_0=node['x_0'],
                                       fwhm=node['fwhm'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'fwhm': _parameter_to_value(model.fwhm)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, physical_models.Drude1D) and
                isinstance(b, physical_models.Drude1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.fwhm, b.fwhm)


class Plummer1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/plummer1d-2.0.0",
            "tag:stsci.edu:asdf/transform/plummer1d-1.0.0",
            }

    types = {physical_models.Plummer1D}

    def from_tree_transform(self, node):
        return physical_models.Plummer1D(mass=node['mass'],
                                         r_plum=node['r_plum'])

    def to_tree_transform(self, model):
        node = {'mass': _parameter_to_value(model.mass),
                'r_plum': _parameter_to_value(model.r_plum)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, physical_models.Plummer1D) and
                isinstance(b, physical_models.Plummer1D))
        assert_array_equal(a.mass, b.mass)
        assert_array_equal(a.r_plum, b.r_plum)
