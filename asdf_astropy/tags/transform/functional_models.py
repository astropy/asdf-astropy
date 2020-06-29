# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

from numpy.testing import assert_array_equal

from astropy.modeling import functional_models
from .basic import TransformConverter
from . import _parameter_to_value


__all__ = ['AiryDisk2DConverter', 'Box1DConverter', 'Box2DConverter',
           'Disk2DConverter', 'Ellipse2DConverter', 'Exponential1DConverter',
           'Gaussian1DConverter', 'Gaussian2DConverter', 'KingProjectedAnalytic1DConverter',
           'Logarithmic1DConverter', 'Lorentz1DConverter', 'Moffat1DConverter',
           'Moffat2DConverter', 'Planar2D', 'RedshiftScaleFactorConverter',
           'RickerWavelet1DConverter', 'RickerWavelet2DConverter', 'Ring2DConverter',
           'Sersic1DConverter', 'Sersic2DConverter', 'Sine1DConverter', 'Trapezoid1DConverter',
           'TrapezoidDisk2DConverter', 'Voigt1DConverter']


class AiryDisk2DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/airy_disk2d-2.0.0",
            "tag:stsci.edu:asdf/transform/airy_disk2d-1.0.0",
            }

    types = {functional_models.AiryDisk2D}

    def from_tree_transform(self, node):
        return functional_models.AiryDisk2D(amplitude=node['amplitude'],
                                            x_0=node['x_0'],
                                            y_0=node['y_0'],
                                            radius=node['radius'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'y_0': _parameter_to_value(model.y_0),
                'radius': _parameter_to_value(model.radius)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.AiryDisk2D) and
                isinstance(b, functional_models.AiryDisk2D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.y_0, b.y_0)
        assert_array_equal(a.radius, b.radius)


class Box1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/box1d-2.0.0",
            "tag:stsci.edu:asdf/transform/box1d-1.0.0",
            }

    types = {functional_models.Box1D}

    def from_tree_transform(self, node):
        return functional_models.Box1D(amplitude=node['amplitude'],
                                       x_0=node['x_0'],
                                       width=node['width'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'width': _parameter_to_value(model.width)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Box1D) and
                isinstance(b, functional_models.Box1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.width, b.width)


class Box2DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/box2d-2.0.0",
            "tag:stsci.edu:asdf/transform/box2d-1.0.0",
            }

    types = {functional_models.Box2D}

    def from_tree_transform(self, node):
        return functional_models.Box2D(amplitude=node['amplitude'],
                                       x_0=node['x_0'],
                                       x_width=node['x_width'],
                                       y_0=node['y_0'],
                                       y_width=node['y_width'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'x_width': _parameter_to_value(model.x_width),
                'y_0': _parameter_to_value(model.y_0),
                'y_width': _parameter_to_value(model.y_width)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Box2D) and
                isinstance(b, functional_models.Box2D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.x_width, b.x_width)
        assert_array_equal(a.y_0, b.y_0)
        assert_array_equal(a.y_width, b.y_width)


class Disk2DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/disk2d-2.0.0",
            "tag:stsci.edu:asdf/transform/disk2d-1.0.0",
            }

    types = {functional_models.Disk2D}

    def from_tree_transform(self, node):
        return functional_models.Disk2D(amplitude=node['amplitude'],
                                        x_0=node['x_0'],
                                        y_0=node['y_0'],
                                        R_0=node['R_0'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'y_0': _parameter_to_value(model.y_0),
                'R_0': _parameter_to_value(model.R_0)}

        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Disk2D) and
                isinstance(b, functional_models.Disk2D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.y_0, b.y_0)
        assert_array_equal(a.R_0, b.R_0)


class Ellipse2DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/ellipse2d-2.0.0",
            "tag:stsci.edu:asdf/transform/ellipse2d-1.0.0",
            }

    types = {functional_models.Ellipse2D}

    def from_tree_transform(self, node):
        return functional_models.Ellipse2D(amplitude=node['amplitude'],
                                           x_0=node['x_0'],
                                           y_0=node['y_0'],
                                           a=node['a'],
                                           b=node['b'],
                                           theta=node['theta'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'y_0': _parameter_to_value(model.y_0),
                'a': _parameter_to_value(model.a),
                'b': _parameter_to_value(model.b),
                'theta': _parameter_to_value(model.theta)}

        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Ellipse2D) and
                isinstance(b, functional_models.Ellipse2D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.y_0, b.y_0)
        assert_array_equal(a.a, b.a)
        assert_array_equal(a.b, b.b)
        assert_array_equal(a.theta, b.theta)


class Exponential1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/exponential1d-2.0.0",
            "tag:stsci.edu:asdf/transform/exponential1d-1.0.0",
            }

    types = {functional_models.Exponential1D}

    def from_tree_transform(self, node):
        return functional_models.Exponential1D(amplitude=node['amplitude'],
                                               tau=node['tau'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'tau': _parameter_to_value(model.tau)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Exponential1D) and
                isinstance(b, functional_models.Exponential1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.tau, b.tau)


class Gaussian1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/gaussian1d-2.0.0",
            "tag:stsci.edu:asdf/transform/gaussian1d-1.0.0",
            }

    types = {functional_models.Gaussian1D}

    def from_tree_transform(self, node):
        return functional_models.Gaussian1D(amplitude=node['amplitude'],
                                            mean=node['mean'],
                                            stddev=node['stddev'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'mean': _parameter_to_value(model.mean),
                'stddev': _parameter_to_value(model.stddev)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Gaussian1D) and
                isinstance(b, functional_models.Gaussian1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.mean, b.mean)
        assert_array_equal(a.stddev, b.stddev)


class Gaussian2DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/gaussian2d-2.0.0",
            "tag:stsci.edu:asdf/transform/gaussian2d-1.0.0",
            }

    types = {functional_models.Gaussian2D}

    def from_tree_transform(self, node):
        return functional_models.Gaussian2D(amplitude=node['amplitude'],
                                            x_mean=node['x_mean'],
                                            y_mean=node['y_mean'],
                                            x_stddev=node['x_stddev'],
                                            y_stddev=node['y_stddev'],
                                            theta=node['theta'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_mean': _parameter_to_value(model.x_mean),
                'y_mean': _parameter_to_value(model.y_mean),
                'x_stddev': _parameter_to_value(model.x_stddev),
                'y_stddev': _parameter_to_value(model.y_stddev),
                'theta': _parameter_to_value(model.theta)}

        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Gaussian2D) and
                isinstance(b, functional_models.Gaussian2D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_mean, b.x_mean)
        assert_array_equal(a.y_mean, b.y_mean)
        assert_array_equal(a.x_stddev, b.x_stddev)
        assert_array_equal(a.y_stddev, b.y_stddev)
        assert_array_equal(a.theta, b.theta)


class KingProjectedAnalytic1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/king_projected_analytic1d-2.0.0",
            "tag:stsci.edu:asdf/transform/king_projected_analytic1d-1.0.0",
            }

    types = {functional_models.KingProjectedAnalytic1D}

    def from_tree_transform(self, node):
        return functional_models.KingProjectedAnalytic1D(
                                            amplitude=node['amplitude'],
                                            r_core=node['r_core'],
                                            r_tide=node['r_tide'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'r_core': _parameter_to_value(model.r_core),
                'r_tide': _parameter_to_value(model.r_tide)}

        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.KingProjectedAnalytic1D) and
                isinstance(b, functional_models.KingProjectedAnalytic1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.r_core, b.r_core)
        assert_array_equal(a.r_tide, b.r_tide)


class Logarithmic1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/logarithmic1d-2.0.0",
            "tag:stsci.edu:asdf/transform/logarithmic1d-1.0.0",
            }

    types = {functional_models.Logarithmic1D}

    def from_tree_transform(self, node):
        return functional_models.Logarithmic1D(amplitude=node['amplitude'],
                                               tau=node['tau'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'tau': _parameter_to_value(model.tau)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Logarithmic1D) and
                isinstance(b, functional_models.Logarithmic1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.tau, b.tau)


class Lorentz1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/lorentz1d-2.0.0",
            "tag:stsci.edu:asdf/transform/lorentz1d-1.0.0",
            }

    types = {functional_models.Lorentz1D}

    def from_tree_transform(self, node):
        return functional_models.Lorentz1D(amplitude=node['amplitude'],
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
        assert (isinstance(a, functional_models.Lorentz1D) and
                isinstance(b, functional_models.Lorentz1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.fwhm, b.fwhm)


class Moffat1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/moffat1d-2.0.0",
            "tag:stsci.edu:asdf/transform/moffat1d-1.0.0",
            }

    types = {functional_models.Moffat1D}

    def from_tree_transform(self, node):
        return functional_models.Moffat1D(amplitude=node['amplitude'],
                                          x_0=node['x_0'],
                                          gamma=node['gamma'],
                                          alpha=node['alpha'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'gamma': _parameter_to_value(model.gamma),
                'alpha': _parameter_to_value(model.alpha)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Moffat1D) and
                isinstance(b, functional_models.Moffat1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.gamma, b.gamma)
        assert_array_equal(a.alpha, b.alpha)


class Moffat2DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/moffat2d-2.0.0",
            "tag:stsci.edu:asdf/transform/moffat2d-1.0.0",
            }

    types = {functional_models.Moffat2D}

    def from_tree_transform(self, node):
        return functional_models.Moffat2D(amplitude=node['amplitude'],
                                          x_0=node['x_0'],
                                          y_0=node['y_0'],
                                          gamma=node['gamma'],
                                          alpha=node['alpha'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'y_0': _parameter_to_value(model.y_0),
                'gamma': _parameter_to_value(model.gamma),
                'alpha': _parameter_to_value(model.alpha)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Moffat2D) and
                isinstance(b, functional_models.Moffat2D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.y_0, b.y_0)
        assert_array_equal(a.gamma, b.gamma)
        assert_array_equal(a.alpha, b.alpha)


class Planar2D(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/planar2d-2.0.0",
            "tag:stsci.edu:asdf/transform/planar2d-1.0.0",
            }

    types = {functional_models.Planar2D}

    def from_tree_transform(self, node):
        return functional_models.Planar2D(slope_x=node['slope_x'],
                                          slope_y=node['slope_y'],
                                          intercept=node['intercept'])

    def to_tree_transform(self, model):
        node = {'slope_x': _parameter_to_value(model.slope_x),
                'slope_y': _parameter_to_value(model.slope_y),
                'intercept': _parameter_to_value(model.intercept)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Planar2D) and
                isinstance(b, functional_models.Planar2D))
        assert_array_equal(a.slope_x, b.slope_x)
        assert_array_equal(a.slope_y, b.slope_y)
        assert_array_equal(a.intercept, b.intercept)


class RedshiftScaleFactorConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/redshift_scale_factor-2.0.0",
            "tag:stsci.edu:asdf/transform/redshift_scale_factor-1.0.0",
            }

    types = {functional_models.RedshiftScaleFactor}

    def from_tree_transform(self, node):
        return functional_models.RedshiftScaleFactor(z=node['z'])

    def to_tree_transform(self, model):
        node = {'z': _parameter_to_value(model.z)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.RedshiftScaleFactor) and
                isinstance(b, functional_models.RedshiftScaleFactor))
        assert_array_equal(a.z, b.z)


class RickerWavelet1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/ricker_wavelet1d-2.0.0",
            "tag:stsci.edu:asdf/transform/ricker_wavelet1d-1.0.0",
            }

    types = {functional_models.RickerWavelet1D}

    def from_tree_transform(self, node):
        return functional_models.RickerWavelet1D(amplitude=node['amplitude'],
                                                 x_0=node['x_0'],
                                                 sigma=node['sigma'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'sigma': _parameter_to_value(model.sigma)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.RickerWavelet1D) and
                isinstance(b, functional_models.RickerWavelet1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.sigma, b.sigma)


class RickerWavelet2DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/ricker_wavelet2d-2.0.0",
            "tag:stsci.edu:asdf/transform/ricker_wavelet2d-1.0.0",
            }

    types = {functional_models.RickerWavelet2D}

    def from_tree_transform(self, node):
        return functional_models.RickerWavelet2D(amplitude=node['amplitude'],
                                                 x_0=node['x_0'],
                                                 y_0=node['y_0'],
                                                 sigma=node['sigma'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'y_0': _parameter_to_value(model.y_0),
                'sigma': _parameter_to_value(model.sigma)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.RickerWavelet2D) and
                isinstance(b, functional_models.RickerWavelet2D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.y_0, b.y_0)
        assert_array_equal(a.sigma, b.sigma)


class Ring2DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/ring2d-2.0.0",
            "tag:stsci.edu:asdf/transform/ring2d-1.0.0",
            }

    types = {functional_models.Ring2D}

    def from_tree_transform(self, node):
        return functional_models.Ring2D(amplitude=node['amplitude'],
                                        x_0=node['x_0'],
                                        y_0=node['y_0'],
                                        r_in=node['r_in'],
                                        width=node['width'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'y_0': _parameter_to_value(model.y_0),
                'r_in': _parameter_to_value(model.r_in),
                'width': _parameter_to_value(model.width)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Ring2D) and
                isinstance(b, functional_models.Ring2D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.y_0, b.y_0)
        assert_array_equal(a.r_in, b.r_in)
        assert_array_equal(a.width, b.width)


class Sersic1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/sersic1d-2.0.0",
            "tag:stsci.edu:asdf/transform/sersic1d-1.0.0",
            }

    types = {functional_models.Sersic1D}

    def from_tree_transform(self, node):
        return functional_models.Sersic1D(amplitude=node['amplitude'],
                                          r_eff=node['r_eff'],
                                          n=node['n'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'r_eff': _parameter_to_value(model.r_eff),
                'n': _parameter_to_value(model.n)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Sersic1D) and
                isinstance(b, functional_models.Sersic1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.r_eff, b.r_eff)
        assert_array_equal(a.n, b.n)


class Sersic2DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/sersic2d-2.0.0",
            "tag:stsci.edu:asdf/transform/sersic2d-1.0.0",
            }
    types = {functional_models.Sersic2D}

    def from_tree_transform(self, node):
        return functional_models.Sersic2D(amplitude=node['amplitude'],
                                          r_eff=node['r_eff'],
                                          n=node['n'],
                                          x_0=node['x_0'],
                                          y_0=node['y_0'],
                                          ellip=node['ellip'],
                                          theta=node['theta'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'r_eff': _parameter_to_value(model.r_eff),
                'n': _parameter_to_value(model.n),
                'x_0': _parameter_to_value(model.x_0),
                'y_0': _parameter_to_value(model.y_0),
                'ellip': _parameter_to_value(model.ellip),
                'theta': _parameter_to_value(model.theta)

                }
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Sersic2D) and
                isinstance(b, functional_models.Sersic2D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.r_eff, b.r_eff)
        assert_array_equal(a.n, b.n)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.y_0, b.y_0)
        assert_array_equal(a.ellip, b.ellip)
        assert_array_equal(a.theta, b.theta)


class Sine1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/sine1d-2.0.0",
            "tag:stsci.edu:asdf/transform/sine1d-1.0.0",
            }

    types = {functional_models.Sine1D}

    def from_tree_transform(self, node):
        return functional_models.Sine1D(amplitude=node['amplitude'],
                                        frequency=node['frequency'],
                                        phase=node['phase'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'frequency': _parameter_to_value(model.frequency),
                'phase': _parameter_to_value(model.phase)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Sine1D) and
                isinstance(b, functional_models.Sine1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.frequency, b.frequency)
        assert_array_equal(a.phase, b.phase)


class Trapezoid1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/trapezoid1d-2.0.0",
            "tag:stsci.edu:asdf/transform/trapezoid1d-1.0.0",
            }

    types = {functional_models.Trapezoid1D}

    def from_tree_transform(self, node):
        return functional_models.Trapezoid1D(amplitude=node['amplitude'],
                                             x_0=node['x_0'],
                                             width=node['width'],
                                             slope=node['slope'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'width': _parameter_to_value(model.width),
                'slope': _parameter_to_value(model.slope)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Trapezoid1D) and
                isinstance(b, functional_models.Trapezoid1D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.width, b.width)
        assert_array_equal(a.slope, b.slope)


class TrapezoidDisk2DConverter(TransformConverter):
    tags = {"http://asdf-format.org/schemas/transform/trapezoid_disk2d-2.0.0",
            "tag:stsci.edu:asdf/transform/trapezoid_disk2d-1.0.0",
            }
    types = {functional_models.TrapezoidDisk2D}

    def from_tree_transform(self, node):
        return functional_models.TrapezoidDisk2D(amplitude=node['amplitude'],
                                                 x_0=node['x_0'],
                                                 y_0=node['y_0'],
                                                 R_0=node['R_0'],
                                                 slope=node['slope'])

    def to_tree_transform(self, model):
        node = {'amplitude': _parameter_to_value(model.amplitude),
                'x_0': _parameter_to_value(model.x_0),
                'y_0': _parameter_to_value(model.y_0),
                'R_0': _parameter_to_value(model.R_0),
                'slope': _parameter_to_value(model.slope)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.TrapezoidDisk2D) and
                isinstance(b, functional_models.TrapezoidDisk2D))
        assert_array_equal(a.amplitude, b.amplitude)
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.y_0, b.y_0)
        assert_array_equal(a.R_0, b.R_0)
        assert_array_equal(a.slope, b.slope)


class Voigt1DConverter(TransformConverter):

    tags = {"http://asdf-format.org/schemas/transform/voigt1d-2.0.0",
            "tag:stsci.edu:asdf/transform/voigt1d-1.0.0",
            }

    types = {functional_models.Voigt1D}

    def from_tree_transform(self, node):
        return functional_models.Voigt1D(x_0=node['x_0'],
                                         amplitude_L=node['amplitude_L'],
                                         fwhm_L=node['fwhm_L'],
                                         fwhm_G=node['fwhm_G'])

    def to_tree_transform(self, model):
        node = {'x_0': _parameter_to_value(model.x_0),
                'amplitude_L': _parameter_to_value(model.amplitude_L),
                'fwhm_L': _parameter_to_value(model.fwhm_L),
                'fwhm_G': _parameter_to_value(model.fwhm_G)}
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        TransformConverter.assert_equal(a, b)
        assert (isinstance(a, functional_models.Voigt1D) and
                isinstance(b, functional_models.Voigt1D))
        assert_array_equal(a.x_0, b.x_0)
        assert_array_equal(a.amplitude_L, b.amplitude_L)
        assert_array_equal(a.fwhm_L, b.fwhm_L)
        assert_array_equal(a.fwhm_G, b.fwhm_G)
