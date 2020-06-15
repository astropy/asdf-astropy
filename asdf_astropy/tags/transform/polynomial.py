# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

import numpy as np
from numpy.testing import assert_array_equal

from asdf.versioning import AsdfVersion

import astropy.units as u
from astropy.modeling import models
from .basic import TransformConverter
from . import _parameter_to_value

__all__ = ['ShiftConverter', 'ScaleConverter', 'Linear1DConverter', 'MultiplyConverter',
           'PolynomialConverterBase', 'OrthoPolynomialConverter']


class ShiftConverter(TransformConverter):
    tags = {"http://asdf-format.org/schemas/transform/shift-2.0.0",
            "tag:stsci.edu:asdf/transform/shift-1.0.0",
            "tag:stsci.edu:asdf/transform/shift-1.1.0",
            "tag:stsci.edu:asdf/transform/shift-1.2.0",
            }
    types = {models.Shift}

    def from_tree_transform(self, node):
        offset = node['offset']
        if not isinstance(offset, u.Quantity) and not np.isscalar(offset):
            raise NotImplementedError(
                "Asdf currently only supports scalar inputs to Shift transform.")

        return models.Shift(offset)

    def to_tree_transform(self, model):
        offset = model.offset
        return {'offset': _parameter_to_value(offset)}

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        assert (isinstance(a, models.Shift) and
                isinstance(b, models.Shift))
        assert_array_equal(a.offset.value, b.offset.value)


class ScaleConverter(TransformConverter):
    tags = {"http://asdf-format.org/schemas/transform/scale-2.0.0",
            "tag:stsci.edu:asdf/transform/scale-1.0.0",
            "tag:stsci.edu:asdf/transform/scale-1.1.0",
            "tag:stsci.edu:asdf/transform/scale-1.2.0",
            }
    types = {models.Scale}

    def from_tree_transform(self, node):
        factor = node['factor']
        if not isinstance(factor, u.Quantity) and not np.isscalar(factor):
            raise NotImplementedError(
                "Asdf currently only supports scalar inputs to Scale transform.")

        return models.Scale(factor)

    def to_tree_transform(self, model):
        factor = model.factor
        return {'factor': _parameter_to_value(factor)}

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        super().assert_equal(a, b)
        assert (isinstance(a, models.Scale) and
                isinstance(b, models.Scale))
        assert_array_equal(a.factor, b.factor)


class MultiplyConverter(TransformConverter):
    tags = {"http://asdf-format.org/schemas/transform/multiplyscale-2.0.0",
            "tag:stsci.edu:asdf/transform/multiplyscale-1.0.0",
            }
    types = {models.Multiply}

    def from_tree_transform(self, node):
        factor = node['factor']
        return models.Multiply(factor)

    def to_tree_transform(self, model):
        factor = model.factor
        return {'factor': _parameter_to_value(factor)}

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        super().assert_equal(a, b)
        assert (isinstance(a, models.Multiply) and
                isinstance(b, models.Multiply))
        assert_array_equal(a.factor, b.factor)


class PolynomialConverterBase(TransformConverter):
    DOMAIN_WINDOW_MIN_VERSION = AsdfVersion("1.2.0")

    tags = {"http://asdf-format.org/schemas/transform/polynomial-2.0.0",
            "tag:stsci.edu:asdf/transform/polynomial-1.0.0",
            "tag:stsci.edu:asdf/transform/polynomial-1.1.0",
            "tag:stsci.edu:asdf/transform/polynomial-1.2.0",
            }
    types = {models.Polynomial1D, models.Polynomial2D}

    def from_tree_transform(self, node):
        coefficients = np.asarray(node['coefficients'])
        n_dim = coefficients.ndim

        if n_dim == 1:
            domain = node.get('domain', None)
            window = node.get('window', None)

            model = models.Polynomial1D(coefficients.size - 1,
                                        domain=domain, window=window)
            model.parameters = coefficients
        elif n_dim == 2:
            x_domain, y_domain = tuple(node.get('domain', (None, None)))
            x_window, y_window = tuple(node.get('window', (None, None)))
            shape = coefficients.shape
            degree = shape[0] - 1
            if shape[0] != shape[1]:
                raise TypeError("Coefficients must be an (n+1, n+1) matrix")

            coeffs = {}
            for i in range(shape[0]):
                for j in range(shape[0]):
                    if i + j < degree + 1:
                        name = 'c' + str(i) + '_' + str(j)
                        coeffs[name] = coefficients[i, j]
            model = models.Polynomial2D(degree,
                                        x_domain=x_domain,
                                        y_domain=y_domain,
                                        x_window=x_window,
                                        y_window=y_window,
                                        **coeffs)
        else:
            raise NotImplementedError(
                "Asdf currently only supports 1D or 2D polynomial transform.")
        return model

    def to_tree_transform(self, model):
        if isinstance(model, models.Polynomial1D):
            coefficients = np.array(model.parameters)
        elif isinstance(model, models.Polynomial2D):
            degree = model.degree
            coefficients = np.zeros((degree + 1, degree + 1))
            for i in range(degree + 1):
                for j in range(degree + 1):
                    if i + j < degree + 1:
                        name = 'c' + str(i) + '_' + str(j)
                        coefficients[i, j] = getattr(model, name).value
        node = {'coefficients': coefficients}
        ndim = model.n_inputs

        if self.version >= PolynomialConverterBase.DOMAIN_WINDOW_MIN_VERSION:
            # Schema versions prior to 1.2 included an unrelated "domain"
            # property.  We can't serialize the new domain values with those
            # versions because they don't validate.
            if ndim == 1:
                if model.domain is not None:
                    node['domain'] = model.domain
                if model.window is not None:
                    node['window'] = model.window
            else:
                if model.x_domain or model.y_domain is not None:
                    node['domain'] = (model.x_domain, model.y_domain)
                if model.x_window or model.y_window is not None:
                    node['window'] = (model.x_window, model.y_window)

        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        super().assert_equal(a, b)
        assert (isinstance(a, (models.Polynomial1D, models.Polynomial2D)) and
                isinstance(b, (models.Polynomial1D, models.Polynomial2D)))
        assert_array_equal(a.parameters, b.parameters)

        if self.version > PolynomialConverterBase.DOMAIN_WINDOW_MIN_VERSION:
            # Schema versions prior to 1.2 are known not to serialize
            # domain or window.
            if isinstance(a, models.Polynomial1D):
                assert a.domain == b.domain
                assert a.window == b.window
            else:
                assert a.x_domain == b.x_domain
                assert a.x_window == b.x_window
                assert a.y_domain == b.y_domain
                assert a.y_window == b.y_window


class OrthoPolynomialConverter(TransformConverter):
    tags = {"http://asdf-format.org/schemas/transform/ortho_polynomial-2.0.0",
            "tag:stsci.edu:asdf/transform/ortho_polynomial-1.0.0",
            }

    types = {models.Legendre1D,
             models.Legendre2D,
             models.Chebyshev1D,
             models.Chebyshev2D,
             models.Hermite1D,
             models.Hermite2D}

    typemap = {models.Legendre1D: ('legendre', 1),
               models.Legendre2D: ('legendre', 2),
               models.Chebyshev1D: ('chebyshev', 1),
               models.Chebyshev2D: ('chebyshev', 2),
               models.Hermite1D: ('hermite', 1),
               models.Hermite2D: ('hermite', 2)
               }

    invtypemap = dict([[v, k] for k, v in typemap.items()])

    def from_tree_transform(self, node):
        coefficients = np.asarray(node['coefficients'])
        n_dim = coefficients.ndim
        poly_type = node['polynomial_type']
        if n_dim == 1:
            domain = node.get('domain', None)
            window = node.get('window', None)
            model = self.invtypemap[(poly_type, n_dim)](coefficients.size - 1,
                                                        domain=domain,
                                                        window=window)
            model.parameters = coefficients
        elif n_dim == 2:
            x_domain, y_domain = tuple(node.get('domain', (None, None)))
            x_window, y_window = tuple(node.get('window', (None, None)))
            coeffs = {}
            shape = coefficients.shape
            x_degree = shape[0] - 1
            y_degree = shape[1] - 1
            for i in range(x_degree + 1):
                for j in range(y_degree + 1):
                    name = f'c{i}_{j}'
                    coeffs[name] = coefficients[i, j]
            model = self.invtypemap[(poly_type, n_dim)](x_degree, y_degree,
                                                        x_domain=x_domain,
                                                        y_domain=y_domain,
                                                        x_window=x_window,
                                                        y_window=y_window,
                                                        **coeffs)
        else:
            raise NotImplementedError(
                "Asdf currently only supports 1D or 2D polynomial transforms.")
        return model

    def to_tree_transform(self, model):
        poly_type = self.typemap[model.__class__][0]
        ndim = model.n_inputs
        if ndim == 1:
            coefficients = np.array(model.parameters)
        else:
            coefficients = np.zeros((model.x_degree + 1, model.y_degree + 1))
            for i in range(model.x_degree + 1):
                for j in range(model.y_degree + 1):
                    name = f'c{i}_{j}'
                    coefficients[i, j] = getattr(model, name).value
        node = {'polynomial_type': poly_type, 'coefficients': coefficients}
        if ndim == 1:
            if model.domain is not None:
                node['domain'] = model.domain
            if model.window is not None:
                node['window'] = model.window
        else:
            if model.x_domain or model.y_domain is not None:
                node['domain'] = (model.x_domain, model.y_domain)
            if model.x_window or model.y_window is not None:
                node['window'] = (model.x_window, model.y_window)
        return node

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        # There should be a more elegant way of doing this
        super().assert_equal(a, b)
        assert ((isinstance(a, (models.Legendre1D,   models.Legendre2D)) and
                 isinstance(b, (models.Legendre1D,   models.Legendre2D))) or
                (isinstance(a, (models.Chebyshev1D,  models.Chebyshev2D)) and
                 isinstance(b, (models.Chebyshev1D,  models.Chebyshev2D))) or
                (isinstance(a, (models.Hermite1D,    models.Hermite2D)) and
                 isinstance(b, (models.Hermite1D,    models.Hermite2D))))
        assert_array_equal(a.parameters, b.parameters)


class Linear1DConverter(TransformConverter):
    tags = {"http://asdf-format.org/schemas/transform/linear1d-2.0.0",
            "tag:stsci.edu:asdf/transform/linear1d-1.0.0",
            }
    types = {models.Linear1D}

    def from_tree_transform(self, node):
        slope = node.get('slope', None)
        intercept = node.get('intercept', None)

        return models.Linear1D(slope=slope, intercept=intercept)

    def to_tree_transform(self, model):
        return {
            'slope': _parameter_to_value(model.slope),
            'intercept': _parameter_to_value(model.intercept),
        }

    def assert_equal(self, a, b):
        # TODO: If models become comparable themselves, remove this.
        super().assert_equal(a, b)
        assert (isinstance(a, models.Linear1D) and
                isinstance(b, models.Linear1D))
        assert_array_equal(a.slope, b.slope)
        assert_array_equal(a.intercept, b.intercept)
