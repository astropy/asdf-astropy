import numpy as np
from packaging.version import parse as parse_version

from asdf_astropy.converters.helpers import parse_tag_version

from .core import TransformConverterBase


class PolynomialConverter(TransformConverterBase):
    """
    ASDF support for serializing the 1D and 2D polynomial models.
    """

    # Schema versions prior to 1.2 included an unrelated "domain"
    # property.  We can't serialize the new domain values with those
    # versions because they don't validate.
    _DOMAIN_WINDOW_MIN_VERSION = parse_version("1.2.0")

    tags = ("tag:stsci.edu:asdf/transform/polynomial-*",)
    types = (
        "astropy.modeling.polynomial.Polynomial1D",
        "astropy.modeling.polynomial.Polynomial2D",
    )

    def to_yaml_tree_transform(self, model, tag, ctx):
        from astropy.modeling.polynomial import Polynomial1D, Polynomial2D

        if isinstance(model, Polynomial1D):
            coefficients = np.array(model.parameters)
        elif isinstance(model, Polynomial2D):
            degree = model.degree
            coefficients = np.zeros((degree + 1, degree + 1))
            for i in range(degree + 1):
                for j in range(degree + 1):
                    if i + j < degree + 1:
                        name = "c" + str(i) + "_" + str(j)
                        coefficients[i, j] = getattr(model, name).value

        node = {"coefficients": coefficients}

        if parse_tag_version(tag) >= self._DOMAIN_WINDOW_MIN_VERSION:
            if model.n_inputs == 1:
                if model.domain is not None:
                    node["domain"] = model.domain
                if model.window is not None:
                    node["window"] = model.window
            else:
                if model.x_domain or model.y_domain is not None:
                    node["domain"] = (model.x_domain, model.y_domain)
                if model.x_window or model.y_window is not None:
                    node["window"] = (model.x_window, model.y_window)

        return node

    def from_yaml_tree_transform(self, node, tag, ctx):
        from astropy.modeling.polynomial import Polynomial1D, Polynomial2D

        coefficients = np.asarray(node["coefficients"])
        n_dim = coefficients.ndim

        if n_dim == 1:
            domain = node.get("domain", None)
            window = node.get("window", None)

            model = Polynomial1D(coefficients.size - 1, domain=domain, window=window)
            model.parameters = coefficients
        elif n_dim == 2:  # noqa: PLR2004
            x_domain, y_domain = tuple(node.get("domain", (None, None)))
            x_window, y_window = tuple(node.get("window", (None, None)))
            shape = coefficients.shape
            degree = shape[0] - 1
            if shape[0] != shape[1]:
                msg = "Coefficients must be an (n+1, n+1) matrix"
                raise TypeError(msg)

            coeffs = {}
            for i in range(shape[0]):
                for j in range(shape[0]):
                    if i + j < degree + 1:
                        name = "c" + str(i) + "_" + str(j)
                        coeffs[name] = coefficients[i, j]
            model = Polynomial2D(
                degree,
                x_domain=x_domain,
                y_domain=y_domain,
                x_window=x_window,
                y_window=y_window,
                **coeffs,
            )
        else:
            msg = "astropy supports only 1D or 2D polynomial models"
            raise NotImplementedError(msg)

        return model


_CLASS_NAME_TO_POLY_INFO = {
    "Legendre1D": ("legendre", 1),
    "Legendre2D": ("legendre", 2),
    "Chebyshev1D": ("chebyshev", 1),
    "Chebyshev2D": ("chebyshev", 2),
    "Hermite1D": ("hermite", 1),
    "Hermite2D": ("hermite", 2),
}

_POLY_INFO_TO_CLASS_NAME = {v: k for k, v in _CLASS_NAME_TO_POLY_INFO.items()}


class OrthoPolynomialConverter(TransformConverterBase):
    """
    ASDF support for serializing models that inherit
    OrthoPolyomialBase.
    """

    # Map of model class name to (polynomial type, number of dimensions) tuple:

    tags = ("tag:stsci.edu:asdf/transform/ortho_polynomial-*",)
    types = (
        "astropy.modeling.polynomial.Legendre1D",
        "astropy.modeling.polynomial.Legendre2D",
        "astropy.modeling.polynomial.Chebyshev1D",
        "astropy.modeling.polynomial.Chebyshev2D",
        "astropy.modeling.polynomial.Hermite1D",
        "astropy.modeling.polynomial.Hermite2D",
    )

    def to_yaml_tree_transform(self, model, tag, ctx):
        poly_type = _CLASS_NAME_TO_POLY_INFO[model.__class__.__name__][0]
        if model.n_inputs == 1:
            coefficients = np.array(model.parameters)
        else:
            coefficients = np.zeros((model.x_degree + 1, model.y_degree + 1))
            for i in range(model.x_degree + 1):
                for j in range(model.y_degree + 1):
                    name = f"c{i}_{j}"
                    coefficients[i, j] = getattr(model, name).value

        node = {"polynomial_type": poly_type, "coefficients": coefficients}

        if model.n_inputs == 1:
            if model.domain is not None:
                node["domain"] = model.domain
            if model.window is not None:
                node["window"] = model.window
        else:
            if model.x_domain or model.y_domain is not None:
                node["domain"] = (model.x_domain, model.y_domain)
            if model.x_window or model.y_window is not None:
                node["window"] = (model.x_window, model.y_window)

        return node

    def from_yaml_tree_transform(self, node, tag, ctx):
        from astropy.modeling import polynomial

        coefficients = np.asarray(node["coefficients"])
        poly_type = node["polynomial_type"]
        n_dim = coefficients.ndim

        class_name = _POLY_INFO_TO_CLASS_NAME[(poly_type, n_dim)]
        model_type = getattr(polynomial, class_name)

        coefficients = np.asarray(node["coefficients"])
        if n_dim == 1:
            domain = node.get("domain", None)
            window = node.get("window", None)
            model = model_type(coefficients.size - 1, domain=domain, window=window)
            model.parameters = coefficients
        elif n_dim == 2:  # noqa: PLR2004
            x_domain, y_domain = tuple(node.get("domain", (None, None)))
            x_window, y_window = tuple(node.get("window", (None, None)))
            coeffs = {}
            shape = coefficients.shape
            x_degree = shape[0] - 1
            y_degree = shape[1] - 1
            for i in range(x_degree + 1):
                for j in range(y_degree + 1):
                    name = f"c{i}_{j}"
                    coeffs[name] = coefficients[i, j]
            model = model_type(
                x_degree,
                y_degree,
                x_domain=x_domain,
                y_domain=y_domain,
                x_window=x_window,
                y_window=y_window,
                **coeffs,
            )
        else:
            msg = "astropy supports only 1D or 2D polynomial models"
            raise NotImplementedError(msg)

        return model
