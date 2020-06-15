# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

from numpy.testing import assert_array_equal

from astropy.modeling import powerlaws
from .basic import TransformConverter
from . import _parameter_to_value


__all__ = ['PowerLaw1DConverter', 'BrokenPowerLaw1DConverter',
           'SmoothlyBrokenPowerLaw1DConverter', 'ExponentialCutoffPowerLaw1DConverter',
           'LogParabola1DConverter']


class PowerLaw1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/power_law1d-2.0.0",
            "tag:stsci.edu:asdf/transform/power_law1d-1.0.0",
            }
    types = {powerlaws.PowerLaw1D}

    def from_tree_transform(self, node):
        return powerlaws.PowerLaw1D(amplitude=node['amplitude'],
                                    x_0=node['x_0'],
                                    alpha=node['alpha'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'alpha': _parameter_to_value(model.alpha)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, powerlaws.PowerLaw1D) and
                isinstance(b, powerlaws.PowerLaw1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.alpha, b.alpha)


class BrokenPowerLaw1DConverter(TransformConverter):
    tags = {"http://asdf-format.org/schemas/transform/broken_power_law1d-2.0.0",
            "tag:stsci.edu:asdf/transform/broken_power_law1d-1.0.0",
            }
    types = {powerlaws.BrokenPowerLaw1D}

    def from_tree_transform(self, node):
        return powerlaws.BrokenPowerLaw1D(amplitude=node['amplitude'],
                                          x_break=node['x_break'],
                                          alpha_1=node['alpha_1'],
                                          alpha_2=node['alpha_2'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_break': _parameter_to_value(model.x_break),
                'alpha_1': _parameter_to_value(model.alpha_1),
                'alpha_2': _parameter_to_value(model.alpha_2)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, powerlaws.BrokenPowerLaw1D) and
                isinstance(b, powerlaws.BrokenPowerLaw1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_break, b.x_break)
        assert_array_equal(a.alpha_1, b.alpha_1)
        assert_array_equal(a.alpha_2, b.alpha_2)


class SmoothlyBrokenPowerLaw1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/smoothly_broken_power_law1d-2.0.0",
            "tag:stsci.edu:asdf/transform/smoothly_broken_power_law1d-1.0.0",
            }

    types = {powerlaws.SmoothlyBrokenPowerLaw1D}

    def from_tree_transform(self, node):
        return powerlaws.SmoothlyBrokenPowerLaw1D(amplitude=node['amplitude'],
                                                  x_break=node['x_break'],
                                                  alpha_1=node['alpha_1'],
                                                  alpha_2=node['alpha_2'],
                                                  delta=node['delta'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_break': _parameter_to_value(model.x_break),
                'alpha_1': _parameter_to_value(model.alpha_1),
                'alpha_2': _parameter_to_value(model.alpha_2),
                'delta': _parameter_to_value(model.delta)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, powerlaws.SmoothlyBrokenPowerLaw1D) and
                isinstance(b, powerlaws.SmoothlyBrokenPowerLaw1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_break, b.x_break)
        assert_array_equal(a.alpha_1, b.alpha_1)
        assert_array_equal(a.alpha_2, b.alpha_2)
        assert_array_equal(a.delta, b.delta)


class ExponentialCutoffPowerLaw1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/exponential_cutoff_power_law1d-2.0.0",
            "tag:stsci.edu:asdf/transform/exponential_cutoff_power_law1d-1.0.0",
            }

    types = {powerlaws.ExponentialCutoffPowerLaw1D}

    def from_tree_transform(self, node):
        return powerlaws.ExponentialCutoffPowerLaw1D(amplitude=node['amplitude'],
                                                     x_0=node['x_0'],
                                                     alpha=node['alpha'],
                                                     x_cutoff=node['x_cutoff'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'alpha': _parameter_to_value(model.alpha),
                'x_cutoff': _parameter_to_value(model.x_cutoff)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, powerlaws.ExponentialCutoffPowerLaw1D) and
                isinstance(b, powerlaws.ExponentialCutoffPowerLaw1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.alpha, b.alpha)
        assert_array_equal(a.x_cutoff, b.x_cutoff)


class LogParabola1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/log_parabola1d-2.0.0",
            "tag:stsci.edu:asdf/transform/log_parabola1d-1.0.0",
            }

    types = {powerlaws.LogParabola1D}

    def from_tree_transform(self, node):
        return powerlaws.LogParabola1D(amplitude=node['amplitude'],
                                       x_0=node['x_0'],
                                       alpha=node['alpha'],
                                       beta=node['beta'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'alpha': _parameter_to_value(model.alpha),
                'beta': _parameter_to_value(model.beta)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, powerlaws.LogParabola1D) and
                isinstance(b, powerlaws.LogParabola1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.alpha, b.alpha)
        assert_array_equal(a.beta, b.beta)
