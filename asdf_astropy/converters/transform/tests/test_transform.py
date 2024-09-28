import itertools
import unittest.mock as mk
import warnings

import asdf
import astropy
import astropy.modeling
import numpy as np
import pytest
from asdf.testing.helpers import yaml_to_asdf
from astropy import units as u
from astropy.modeling import bind_bounding_box
from astropy.modeling import models as astropy_models
from astropy.modeling.bounding_box import CompoundBoundingBox, ModelBoundingBox
from astropy.utils import minversion

from asdf_astropy import integration
from asdf_astropy.testing import helpers


def assert_bounding_box_roundtrip(bounding_box, tmp_path, version=None):
    message = (
        "asdf_astropy.converters.transforms.tests.test_transform.assert_bounding_box_round_trip is deprecated."
        "Use asdf_astropy.testing.helpers.assert_bounding_box_roundtrip instead."
    )
    warnings.warn(message, DeprecationWarning, stacklevel=2)

    return helpers.assert_bounding_box_roundtrip(bounding_box, tmp_path, version=version)


def assert_model_roundtrip(model, tmp_path, version=None):
    message = (
        "asdf_astropy.converters.transforms.tests.test_transform.assert_model_round_trip is deprecated."
        "Use asdf_astropy.testing.helpers.assert_model_roundtrip instead."
    )
    warnings.warn(message, DeprecationWarning, stacklevel=2)

    return helpers.assert_model_roundtrip(model, tmp_path, version=version)


def test_deprecations(tmp_path):
    # Test assert_bounding_box_roundtrip deprecation
    bbox = ModelBoundingBox((0, 1), astropy_models.Polynomial1D(1))
    with pytest.warns(DeprecationWarning, match=".*assert_bounding_box_roundtrip.*"):
        assert_bounding_box_roundtrip(bbox, tmp_path)

    # Test assert_model_roundtrip deprecation
    model = astropy_models.Gaussian2D()
    with pytest.warns(DeprecationWarning, match=".*assert_model_roundtrip.*"):
        assert_model_roundtrip(model, tmp_path)


def create_bounding_boxes():
    model_bounding_box = [
        ModelBoundingBox((0, 1), astropy_models.Polynomial1D(1)),
        ModelBoundingBox(((2, 3), (3, 4)), astropy_models.Polynomial2D(1)),
        ModelBoundingBox(((5, 6), (7, 8)), astropy_models.Polynomial2D(1), order="F"),
    ]

    model_bounding_box.extend(
        [
            ModelBoundingBox((9, 10), astropy_models.Polynomial2D(1), ignored=["x"]),
            ModelBoundingBox((11, 12), astropy_models.Polynomial2D(1), ignored=["y"]),
        ],
    )

    compound_bounding_box = [
        CompoundBoundingBox({(1,): (0, 1), (2,): (2, 3)}, astropy_models.Polynomial2D(1), [("x", True)]),
        CompoundBoundingBox(
            {(1,): ((0, 1), (-1, 0)), (2,): ((2, 3), (-3, -2))},
            astropy_models.Polynomial2D(1),
            [("x", False)],
        ),
        CompoundBoundingBox(
            {(1,): (0, 1), (2,): (2, 3)},
            astropy_models.Polynomial2D(1),
            [("x", False)],
            ignored=["x"],
        ),
        CompoundBoundingBox(
            {(1,): (0, 1), (2,): (2, 3)},
            astropy_models.Polynomial2D(1),
            [("x", False)],
            ignored=["y"],
        ),
    ]

    return model_bounding_box + compound_bounding_box


@pytest.mark.parametrize("bbox", create_bounding_boxes())
def test_round_trip_bounding_box(bbox, tmp_path):
    helpers.assert_bounding_box_roundtrip(bbox, tmp_path)


def create_single_models():  # noqa: PLR0915
    model_with_bounding_box = astropy_models.Shift(10)
    model_with_bounding_box.bounding_box = ((1, 7),)

    model_with_user_inverse = astropy_models.Shift(10)
    model_with_user_inverse.inverse = astropy_models.Shift(-7)

    model_with_constraints = astropy_models.Legendre2D(
        x_degree=1,
        y_degree=1,
        c0_0=1,
        c0_1=2,
        c1_0=3,
        fixed={"c1_0": True, "c0_1": True},
        bounds={"c0_0": (-10, 10)},
    )

    model_with_custom_inputs_outputs = astropy_models.Gaussian2D()
    model_with_custom_inputs_outputs.inputs = ("a", "b")
    model_with_custom_inputs_outputs.outputs = ("c",)

    result = [
        # Generic model features
        astropy_models.Shift(10, name="some model name"),
        model_with_bounding_box,
        model_with_user_inverse,
        model_with_constraints,
        model_with_custom_inputs_outputs,
        # astropy.modeling.functional_models
        astropy_models.AiryDisk2D(amplitude=10.0, x_0=0.5, y_0=1.5),
        astropy_models.Box1D(amplitude=10.0, x_0=0.5, width=5.0),
        astropy_models.Box2D(amplitude=10.0, x_0=0.5, x_width=5.0, y_0=1.5, y_width=7.0),
        astropy_models.Const1D(amplitude=5.0),
        astropy_models.Const2D(amplitude=5.0),
        astropy_models.Disk2D(amplitude=10.0, x_0=0.5, y_0=1.5, R_0=5.0),
        astropy_models.Ellipse2D(amplitude=10.0, x_0=0.5, y_0=1.5, a=2.0, b=4.0, theta=0.1),
        astropy_models.Exponential1D(amplitude=10.0, tau=3.5),
        astropy_models.Gaussian1D(amplitude=10.0, mean=5.0, stddev=3.0),
        astropy_models.Gaussian2D(amplitude=10.0, x_mean=5.0, y_mean=5.0, x_stddev=3.0, y_stddev=3.0),
        astropy_models.KingProjectedAnalytic1D(amplitude=10.0, r_core=5.0, r_tide=2.0),
        astropy_models.Linear1D(slope=2.0, intercept=1.5),
        astropy_models.Logarithmic1D(amplitude=10.0, tau=3.5),
        astropy_models.Lorentz1D(amplitude=10.0, x_0=0.5, fwhm=2.5),
        astropy_models.Moffat1D(amplitude=10.0, x_0=0.5, gamma=1.2, alpha=2.5),
        astropy_models.Moffat2D(amplitude=10.0, x_0=0.5, y_0=1.5, gamma=1.2, alpha=2.5),
        astropy_models.Multiply(3),
        astropy_models.Multiply(10 * u.m),
        astropy_models.Planar2D(slope_x=0.5, slope_y=1.2, intercept=2.5),
        astropy_models.RedshiftScaleFactor(z=2.5),
        astropy_models.RickerWavelet1D(amplitude=10.0, x_0=0.5, sigma=1.2),
        astropy_models.RickerWavelet2D(amplitude=10.0, x_0=0.5, y_0=1.5, sigma=1.2),
        astropy_models.Ring2D(amplitude=10.0, x_0=0.5, y_0=1.5, r_in=5.0, width=10.0),
        astropy_models.Scale(3.4),
        astropy_models.Sersic1D(amplitude=10.0, r_eff=1.0, n=4.0),
        astropy_models.Sersic2D(amplitude=10.0, r_eff=1.0, n=4.0, x_0=0.5, y_0=1.5, ellip=0.0, theta=0.0),
        astropy_models.Shift(2.0),
        astropy_models.Shift(2.0 * u.deg),
        astropy_models.Scale(3.4 * u.deg),
        astropy_models.Sine1D(amplitude=10.0, frequency=0.5, phase=1.0),
        astropy_models.Cosine1D(amplitude=10.0, frequency=0.5, phase=1.0),
        astropy_models.Tangent1D(amplitude=10.0, frequency=0.5, phase=1.0),
        astropy_models.ArcSine1D(amplitude=10.0, frequency=0.5, phase=1.0),
        astropy_models.ArcCosine1D(amplitude=10.0, frequency=0.5, phase=1.0),
        astropy_models.ArcTangent1D(amplitude=10.0, frequency=0.5, phase=1.0),
        astropy_models.Trapezoid1D(amplitude=10.0, x_0=0.5, width=5.0, slope=1.0),
        astropy_models.TrapezoidDisk2D(amplitude=10.0, x_0=0.5, y_0=1.5, R_0=5.0, slope=1.0),
        astropy_models.Voigt1D(x_0=0.55, amplitude_L=10.0, fwhm_L=0.5, fwhm_G=0.9),
        # astropy.modeling.mappings
        astropy_models.Identity(2),
        astropy_models.Mapping((0, 1), n_inputs=3),
        # astropy.modeling.math_functions
        astropy.modeling.math_functions.AbsoluteUfunc(),
        astropy.modeling.math_functions.AddUfunc(),
        astropy.modeling.math_functions.ArccosUfunc(),
        astropy.modeling.math_functions.ArccoshUfunc(),
        astropy.modeling.math_functions.ArcsinUfunc(),
        astropy.modeling.math_functions.ArcsinhUfunc(),
        astropy.modeling.math_functions.Arctan2Ufunc(),
        astropy.modeling.math_functions.ArctanUfunc(),
        astropy.modeling.math_functions.ArctanhUfunc(),
        astropy.modeling.math_functions.CbrtUfunc(),
        astropy.modeling.math_functions.CosUfunc(),
        astropy.modeling.math_functions.CoshUfunc(),
        astropy.modeling.math_functions.Deg2radUfunc(),
        astropy.modeling.math_functions.DivideUfunc(),
        astropy.modeling.math_functions.DivmodUfunc(),
        astropy.modeling.math_functions.Exp2Ufunc(),
        astropy.modeling.math_functions.ExpUfunc(),
        astropy.modeling.math_functions.Expm1Ufunc(),
        astropy.modeling.math_functions.FabsUfunc(),
        astropy.modeling.math_functions.Floor_divideUfunc(),
        astropy.modeling.math_functions.FmodUfunc(),
        astropy.modeling.math_functions.HypotUfunc(),
        astropy.modeling.math_functions.Log10Ufunc(),
        astropy.modeling.math_functions.Log1pUfunc(),
        astropy.modeling.math_functions.Log2Ufunc(),
        astropy.modeling.math_functions.LogUfunc(),
        astropy.modeling.math_functions.Logaddexp2Ufunc(),
        astropy.modeling.math_functions.LogaddexpUfunc(),
        astropy.modeling.math_functions.ModUfunc(),
        astropy.modeling.math_functions.MultiplyUfunc(),
        astropy.modeling.math_functions.NegativeUfunc(),
        astropy.modeling.math_functions.PositiveUfunc(),
        astropy.modeling.math_functions.PowerUfunc(),
        astropy.modeling.math_functions.Rad2degUfunc(),
        astropy.modeling.math_functions.ReciprocalUfunc(),
        astropy.modeling.math_functions.RemainderUfunc(),
        astropy.modeling.math_functions.RintUfunc(),
        astropy.modeling.math_functions.SinUfunc(),
        astropy.modeling.math_functions.SinhUfunc(),
        astropy.modeling.math_functions.SqrtUfunc(),
        astropy.modeling.math_functions.SquareUfunc(),
        astropy.modeling.math_functions.SubtractUfunc(),
        astropy.modeling.math_functions.TanUfunc(),
        astropy.modeling.math_functions.TanhUfunc(),
        astropy.modeling.math_functions.True_divideUfunc(),
        # astropy.modeling.physical_models
        astropy_models.BlackBody(scale=10.0, temperature=6000.0 * u.K),
        astropy_models.Drude1D(amplitude=10.0, x_0=0.5, fwhm=2.5),
        # TODO: NFW
        # astropy.modeling.polynomial
        astropy_models.Chebyshev1D(2, c0=2, c1=3, c2=0.5),
        astropy_models.Chebyshev1D(2, c0=2, c1=3, c2=0.5, domain=(0.0, 1.0), window=(1.5, 2.5)),
        astropy_models.Chebyshev2D(1, 1, c0_0=1, c0_1=2, c1_0=3),
        astropy_models.Chebyshev2D(
            1,
            1,
            c0_0=1,
            c0_1=2,
            c1_0=3,
            x_domain=(1.0, 2.0),
            y_domain=(3.0, 4.0),
            x_window=(5.0, 6.0),
            y_window=(7.0, 8.0),
        ),
        astropy_models.Hermite1D(2, c0=2, c1=3, c2=0.5),
        astropy_models.Hermite2D(1, 1, c0_0=1, c0_1=2, c1_0=3),
        astropy_models.Legendre1D(2, c0=2, c1=3, c2=0.5),
        astropy_models.Legendre2D(1, 1, c0_0=1, c0_1=2, c1_0=3),
        astropy_models.Polynomial1D(2, c0=1, c1=2, c2=3),
        astropy_models.Polynomial2D(1, c0_0=1, c0_1=2, c1_0=3),
        # astropy.modeling.spline
        astropy_models.Spline1D(
            np.array([-3.0, -3.0, -3.0, -3.0, -1.0, 0.0, 1.0, 3.0, 3.0, 3.0, 3.0]),
            np.array(
                [
                    0.10412331,
                    0.07013616,
                    -0.18799552,
                    1.35953147,
                    -0.15282581,
                    0.03923,
                    -0.04297299,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                ],
            ),
            3,
        ),
        # astropy.modeling.powerlaws
        astropy_models.BrokenPowerLaw1D(amplitude=10, x_break=0.5, alpha_1=2.0, alpha_2=3.5),
        astropy_models.ExponentialCutoffPowerLaw1D(10, 0.5, 2.0, 7.0),
        astropy_models.LogParabola1D(
            amplitude=10,
            x_0=0.5,
            alpha=2.0,
            beta=3.0,
        ),
        astropy_models.PowerLaw1D(amplitude=10.0, x_0=0.5, alpha=2.0),
        astropy_models.SmoothlyBrokenPowerLaw1D(amplitude=10.0, x_break=5.0, alpha_1=2.0, alpha_2=3.0, delta=0.5),
        # astropy.modeling.projections
        astropy_models.AffineTransformation2D(
            matrix=np.array([[1.0, 2.0], [3.0, 4.0]]),
            translation=np.array([5.0, 6.0]),
        ),
        astropy_models.Pix2Sky_Airy(theta_b=75.8),
        astropy_models.Sky2Pix_Airy(theta_b=75.8),
        astropy_models.Pix2Sky_BonneEqualArea(theta1=44.3),
        astropy_models.Sky2Pix_BonneEqualArea(theta1=44.3),
        astropy_models.Pix2Sky_COBEQuadSphericalCube(),
        astropy_models.Sky2Pix_COBEQuadSphericalCube(),
        astropy_models.Pix2Sky_ConicEqualArea(sigma=89.5, delta=0.5),
        astropy_models.Sky2Pix_ConicEqualArea(sigma=89.5, delta=0.5),
        astropy_models.Pix2Sky_ConicEquidistant(sigma=89.5, delta=0.5),
        astropy_models.Sky2Pix_ConicEquidistant(sigma=89.5, delta=0.5),
        astropy_models.Pix2Sky_ConicOrthomorphic(sigma=88.0, delta=1.0),
        astropy_models.Sky2Pix_ConicOrthomorphic(sigma=88.0, delta=1.0),
        astropy_models.Pix2Sky_ConicPerspective(sigma=89.5, delta=0.5),
        astropy_models.Sky2Pix_ConicPerspective(sigma=89.5, delta=0.5),
        astropy_models.Pix2Sky_CylindricalEqualArea(lam=0.5),
        astropy_models.Sky2Pix_CylindricalEqualArea(lam=0.5),
        astropy_models.Pix2Sky_CylindricalPerspective(mu=1.5, lam=2.4),
        astropy_models.Sky2Pix_CylindricalPerspective(mu=1.5, lam=2.4),
        astropy_models.Pix2Sky_Gnomonic(),
        astropy_models.Sky2Pix_Gnomonic(),
        astropy_models.Pix2Sky_HEALPixPolar(),
        astropy_models.Sky2Pix_HEALPixPolar(),
        astropy_models.Pix2Sky_HEALPix(H=12.0, X=17.0),
        astropy_models.Sky2Pix_HEALPix(H=12.0, X=17.0),
        astropy_models.Pix2Sky_HammerAitoff(),
        astropy_models.Sky2Pix_HammerAitoff(),
        astropy_models.Pix2Sky_Mercator(),
        astropy_models.Sky2Pix_Mercator(),
        astropy_models.Pix2Sky_Molleweide(),
        astropy_models.Sky2Pix_Molleweide(),
        astropy_models.Pix2Sky_Parabolic(),
        astropy_models.Sky2Pix_Parabolic(),
        astropy_models.Pix2Sky_PlateCarree(),
        astropy_models.Sky2Pix_PlateCarree(),
        astropy_models.Pix2Sky_Polyconic(),
        astropy_models.Sky2Pix_Polyconic(),
        astropy_models.Pix2Sky_QuadSphericalCube(),
        astropy_models.Sky2Pix_QuadSphericalCube(),
        astropy_models.Pix2Sky_SansonFlamsteed(),
        astropy_models.Sky2Pix_SansonFlamsteed(),
        astropy_models.Pix2Sky_SlantOrthographic(xi=0.1, eta=0.2),
        astropy_models.Sky2Pix_SlantOrthographic(xi=0.1, eta=0.2),
        astropy_models.Pix2Sky_SlantZenithalPerspective(mu=1.5, phi0=15.0, theta0=80.0),
        astropy_models.Sky2Pix_SlantZenithalPerspective(mu=1.5, phi0=15.0, theta0=80.0),
        astropy_models.Pix2Sky_Stereographic(),
        astropy_models.Sky2Pix_Stereographic(),
        astropy_models.Pix2Sky_TangentialSphericalCube(),
        astropy_models.Sky2Pix_TangentialSphericalCube(),
        astropy_models.Pix2Sky_ZenithalEqualArea(),
        astropy_models.Sky2Pix_ZenithalEqualArea(),
        astropy_models.Pix2Sky_ZenithalEquidistant(),
        astropy_models.Sky2Pix_ZenithalEquidistant(),
        astropy_models.Pix2Sky_ZenithalPerspective(mu=1.5, gamma=15.0),
        astropy_models.Sky2Pix_ZenithalPerspective(mu=1.5, gamma=15.0),
        # astropy.modeling.rotations
        astropy_models.EulerAngleRotation(23, 14, 2.3, axes_order="xzx"),
        astropy_models.RotateCelestial2Native(5.63, -72.5, 180),
        astropy_models.RotateCelestial2Native(5.63 * u.deg, -72.5 * u.deg, 180 * u.deg),
        astropy_models.RotateNative2Celestial(5.63, -72.5, 180),
        astropy_models.RotateNative2Celestial(5.63 * u.deg, -72.5 * u.deg, 180 * u.deg),
        astropy_models.Rotation2D(angle=1.51),
        astropy_models.RotationSequence3D([1.2, 2.3, 3.4, 0.3], "xyzx"),
        astropy_models.SphericalRotationSequence([1.2, 2.3, 3.4, 0.3], "xyzy"),
        # astropy.modeling.tabular
        astropy_models.Tabular1D(points=np.arange(0, 5), lookup_table=[1.0, 10, 2, 45, -3]),
        astropy_models.Tabular1D(points=np.arange(0, 5) * u.pix, lookup_table=[1.0, 10, 2, 45, -3] * u.nm),
        astropy_models.Tabular2D(
            points=([1, 2, 3], [1, 2, 3]),
            lookup_table=np.arange(0, 9).reshape(3, 3),
            bounds_error=False,
            fill_value=None,
            method="nearest",
        ),
        astropy_models.Tabular2D(
            points=([1, 2, 3], [1, 2, 3]) * u.pix,
            lookup_table=np.arange(0, 9).reshape(3, 3) * u.nm,
            bounds_error=False,
            fill_value=None,
            method="nearest",
        ),
    ]

    # Test case for model with a metaclass generated abstract bounding_box
    # where a custom bounding box is stored
    gaussian_1d = astropy_models.Gaussian1D(10, 1.5, 0.25)
    gaussian_1d.bounding_box = [7, 8]
    result.append(gaussian_1d)

    # compound model with bounding box
    model = astropy_models.Shift(1) & astropy_models.Shift(2)
    model.bounding_box = ((1, 2), (3, 4))
    result.append(model)

    # compound model with bounding box
    model = astropy_models.Shift(1) & astropy_models.Shift(2) & astropy_models.Shift(3)
    model.bounding_box = ((1, 2), (3, 4), (5, 6))
    result.append(model)

    # model with compound bounding box
    model = astropy_models.Shift(1) & astropy_models.Scale(2) & astropy_models.Identity(1)
    model.inputs = ("x", "y", "slit_id")
    bounding_boxes = {
        (0,): ((-0.5, 1047.5), (-0.5, 2047.5)),
        (1,): ((-0.5, 3047.5), (-0.5, 4047.5)),
    }
    bounding_box = CompoundBoundingBox.validate(model, bounding_boxes, selector_args=[("slit_id", True)], order="F")
    model.bounding_box = bounding_box
    result.append(model)

    model = astropy_models.Shift(1) & astropy_models.Shift(2) & astropy_models.Shift(3)
    model.inputs = ("x", "y", "z")
    bounding_boxes = {
        (0,): (1.0, 2.0),
        (1,): (3.0, 4.0),
    }

    bounding_box = CompoundBoundingBox.validate(
        model,
        bounding_boxes,
        selector_args=[("x", True)],
        ignored=["y"],
    )
    model.bounding_box = bounding_box
    result.append(model)

    result.append(astropy_models.Plummer1D(mass=10.0, r_plum=5.0))

    # models with input_units_equivalencies
    # 1D model
    m1 = astropy_models.Shift(1 * u.kg)
    m1.input_units_equivalencies = {"x": u.mass_energy()}

    # 2D model
    m2 = astropy_models.Const2D(10 * u.Hz)
    m2.input_units_equivalencies = {"x": u.dimensionless_angles(), "y": u.dimensionless_angles()}

    # 2D model with only one input equivalencies
    m3 = astropy_models.Const2D(10 * u.Hz)
    m3.input_units_equivalencies = {"x": u.dimensionless_angles()}

    # model using equivalency that has args using units
    m4 = astropy_models.PowerLaw1D(amplitude=1 * u.m, x_0=10 * u.pix, alpha=7)
    m4.input_units_equivalencies = {"x": u.equivalencies.pixel_scale(0.5 * u.arcsec / u.pix)}

    result.extend([m1, m2, m3, m4])

    # compound models with input_units_equivalencies
    m1 = astropy_models.Gaussian1D(10 * u.K, 11 * u.arcsec, 12 * u.arcsec)
    m1.input_units_equivalencies = {"x": u.parallax()}
    m2 = astropy_models.Gaussian1D(5 * u.s, 2 * u.K, 3 * u.K)
    m2.input_units_equivalencies = {"x": u.temperature()}

    result.extend([m1 | m2, m1 & m2, m1 + m2])

    # fix_inputs models with input_units_equivalencies
    m1 = astropy_models.Pix2Sky_TAN()
    m1.input_units_equivalencies = {"x": u.dimensionless_angles(), "y": u.dimensionless_angles()}
    m2 = astropy_models.Rotation2D()
    m = m1 | m2

    result.extend([astropy_models.fix_inputs(m, {"x": 45}), astropy_models.fix_inputs(m, {0: 45})])

    result.append(astropy_models.Schechter1D(phi_star=1.0, m_star=2.0, alpha=3.0))

    return result


UNSUPPORTED_MODELS = [
    # FITS-specific and deemed unworthy of ASDF serialization:
    astropy.modeling.polynomial.InverseSIP,
    astropy.modeling.polynomial.SIP,
    # Base classes which should not be directly supported:
    astropy.modeling.core.Model,
    astropy.modeling.math_functions._NPUfuncModel,
    astropy.modeling.polynomial.OrthoPolynomialBase,
    astropy.modeling.polynomial.PolynomialModel,
    astropy.modeling.projections.Conic,
    astropy.modeling.projections.Cylindrical,
    astropy.modeling.projections.HEALPix,
    astropy.modeling.projections.Pix2SkyProjection,
    astropy.modeling.projections.Projection,
    astropy.modeling.projections.PseudoConic,
    astropy.modeling.projections.PseudoCylindrical,
    astropy.modeling.projections.QuadCube,
    astropy.modeling.projections.Sky2PixProjection,
    astropy.modeling.projections.Zenithal,
    # https://github.com/astropy/asdf-astropy/issues/6
    astropy.modeling.physical_models.NFW,
]

if minversion("astropy", "6.0.dev"):
    UNSUPPORTED_MODELS.append(astropy.modeling.functional_models.GeneralSersic2D)

if minversion("astropy", "7.0.dev"):
    UNSUPPORTED_MODELS.append(astropy.modeling.functional_models.Lorentz2D)


@pytest.mark.parametrize("model", create_single_models())
def test_single_model(tmp_path, model):
    helpers.assert_model_roundtrip(model, tmp_path)


def get_all_models():
    def _iterate_model_classes():
        for _key, value in itertools.chain(
            astropy_models.__dict__.items(),
            astropy.modeling.math_functions.__dict__.items(),
        ):
            if (
                isinstance(value, type)
                and issubclass(value, astropy.modeling.core.Model)
                and value not in UNSUPPORTED_MODELS
            ):
                yield value

    return list(_iterate_model_classes())


@pytest.mark.parametrize("model", get_all_models())
def test_all_models_supported(model):
    """
    Test that all model classes in astropy have serialization
    support implemented in this package.  If this test fails,
    file an issue on GitHub for each missing model and add
    the model to the UNSUPPORTED_MODELS list above with
    a link to the issue in a comment.
    """

    extensions = integration.get_extensions()
    extension_manager = asdf.extension.ExtensionManager(extensions)

    message = f"Missing support for model: {model.__module__}.{model.__qualname__}"
    assert extension_manager.handles_type(model), message


def test_legacy_const(tmp_path):
    with asdf.config_context() as config:
        config.remove_extension("asdf://asdf-format.org/transform/extensions/transform-1.6.0")
        config.remove_extension("asdf://asdf-format.org/transform/extensions/transform-1.5.0")

        model = astropy_models.Const1D(amplitude=5.0)
        helpers.assert_model_roundtrip(model, tmp_path, version="1.3.0")

        model = astropy_models.Const2D(amplitude=5.0)
        with pytest.raises(TypeError, match=r".* does not support models with > 1 dimension"):
            helpers.assert_model_roundtrip(model, tmp_path, version="1.3.0")


COMPOUND_OPERATORS = [
    "__add__",
    "__sub__",
    "__mul__",
    "__truediv__",
    "__pow__",
    "__or__",
    "__and__",
]


@pytest.mark.parametrize("operator", COMPOUND_OPERATORS)
def test_compound_model(tmp_path, operator):
    left_model = astropy_models.Shift(5)
    right_model = astropy_models.Shift(-1)
    model = getattr(left_model, operator)(right_model)
    result = helpers.assert_model_roundtrip(model, tmp_path)
    helpers.assert_model_equal(result.left, left_model)
    helpers.assert_model_equal(result.right, right_model)
    assert result.op == model.op


def test_fix_inputs(tmp_path):
    model = astropy_models.Gaussian2D(1, 2, 3, 4, 5)
    fixed_model = astropy_models.fix_inputs(model, {"x": 2.5})
    result = helpers.assert_model_roundtrip(fixed_model, tmp_path)
    helpers.assert_model_equal(result.left, model)
    assert result.right == fixed_model.right
    assert result.op == fixed_model.op


def test_units_mapping(tmp_path):
    # Basic mapping between units:
    model = astropy_models.UnitsMapping(((u.m, u.dimensionless_unscaled),))
    model.name = "foo"
    result = helpers.assert_model_roundtrip(model, tmp_path)
    assert result.mapping == model.mapping

    # Remove units:
    model = astropy_models.UnitsMapping(((u.m, None),))
    result = helpers.assert_model_roundtrip(model, tmp_path)
    assert result.mapping == model.mapping

    # Change a model to accept any units:
    model = astropy_models.UnitsMapping(((None, u.m),))
    result = helpers.assert_model_roundtrip(model, tmp_path)
    assert result.mapping == model.mapping

    # With equivalencies:
    model = astropy_models.UnitsMapping(
        ((u.m, u.dimensionless_unscaled),),
        input_units_equivalencies={"x": u.equivalencies.spectral()},
    )
    result = helpers.assert_model_roundtrip(model, tmp_path)
    assert result.mapping == model.mapping

    # Allow dimensionless on all inputs:
    model = astropy_models.UnitsMapping(
        ((u.m, u.dimensionless_unscaled), (u.s, u.Hz)),
        input_units_allow_dimensionless=True,
    )
    result = helpers.assert_model_roundtrip(model, tmp_path)
    assert result.mapping == model.mapping

    # Allow dimensionless selectively:
    model = astropy_models.UnitsMapping(
        ((u.m, u.dimensionless_unscaled), (u.s, u.Hz)),
        input_units_allow_dimensionless={"x0": True, "x1": False},
    )
    result = helpers.assert_model_roundtrip(model, tmp_path)
    assert result.mapping == model.mapping


@pytest.mark.parametrize("standard_version", [v for v in asdf.versioning.supported_versions if v >= "1.4.0"])
@pytest.mark.parametrize(
    "model",
    [
        astropy_models.Polynomial1D(1, c0=5, c1=17),
        astropy_models.Polynomial1D(1, c0=5, c1=17, domain=[-5, 4], window=[-2, 3]),
        astropy_models.Chebyshev1D(2, c0=2, c1=3, c2=0.5, domain=[-2, 2]),
        astropy_models.Chebyshev1D(2, c0=2, c1=3, c2=0.5, domain=[-2, 2], window=[-0.5, 0.5]),
    ],
)
def test_1d_polynomial_with_asdf_standard_version(tmp_path, standard_version, model):
    result = helpers.assert_model_roundtrip(model, tmp_path, version=standard_version)
    assert result.domain == model.domain
    assert result.window == model.window


@pytest.mark.parametrize("standard_version", [v for v in asdf.versioning.supported_versions if v >= "1.4.0"])
@pytest.mark.parametrize(
    "model",
    [
        astropy_models.Polynomial2D(2, c0_0=3, c1_0=5, c0_1=7),
        astropy_models.Polynomial2D(
            2,
            c0_0=3,
            c1_0=5,
            c0_1=7,
            x_domain=[-2, 2],
            y_domain=[-4, 4],
            x_window=[-6, 6],
            y_window=[-8, 8],
        ),
        astropy_models.Chebyshev2D(1, 1, c0_0=1, c0_1=2, c1_0=3, x_domain=[-2, 2], y_domain=[-2, 2]),
        astropy_models.Chebyshev2D(
            1,
            1,
            c0_0=1,
            c0_1=2,
            c1_0=3,
            x_domain=[-2, 2],
            y_domain=[-2, 2],
            x_window=[-0.5, 0.5],
            y_window=[-0.1, 0.5],
        ),
    ],
)
def test_2d_polynomial_with_asdf_standard_version(tmp_path, standard_version, model):
    result = helpers.assert_model_roundtrip(model, tmp_path, version=standard_version)
    assert result.x_domain == model.x_domain
    assert result.y_domain == model.y_domain
    assert result.x_window == model.x_window
    assert result.y_window == model.y_window


def test_deserialize_compound_user_inverse(tmp_path):
    """
    Confirm that we are able to correctly reconstruct a
    compound model with a user inverse set on one of its
    component models.

    Due to code in TransformConverter that facilitates circular
    inverses, the user inverse of the component model is
    not available at the time that the CompoundModel is
    constructed.
    """

    yaml = """
model: !transform/concatenate-1.2.0
  forward:
  - !transform/shift-1.2.0
    inverse: !transform/shift-1.2.0 {offset: 5.0}
    offset: -10.0
  - !transform/shift-1.2.0 {offset: -20.0}
  """
    buff = yaml_to_asdf(yaml)
    with asdf.open(buff) as af:
        model = af["model"]
        assert model.has_inverse()
        assert model.inverse(-5, -20) == (0, 0)


def test_rotation_errors():
    from asdf_astropy.converters.transform.rotations import RotationSequenceConverter

    converter = RotationSequenceConverter()

    # to yaml error
    mdl = astropy_models.Const1D(5)
    mdl.angles = mk.MagicMock()
    mdl.axes_order = mk.MagicMock()
    with pytest.raises(TypeError, match=r"Cannot serialize model of type *"):
        converter.to_yaml_tree_transform(mdl, mk.MagicMock(), mk.MagicMock())

    # from yaml error
    node = {"angles": mk.MagicMock(), "axes_order": mk.MagicMock(), "rotation_type": mk.MagicMock()}
    with pytest.raises(ValueError, match=r"Unrecognized rotation_type: *"):
        converter.from_yaml_tree_transform(node, mk.MagicMock(), mk.MagicMock())


def test_projection_errors():
    from asdf_astropy.converters.transform.projections import ProjectionConverter

    converter = ProjectionConverter(mk.MagicMock(), mk.MagicMock(), mk.MagicMock())
    converter._sky2pix_type = astropy_models.Pix2Sky_Airy
    converter._pix2sky_type = astropy_models.Sky2Pix_Airy

    # to yaml error
    mdl = astropy_models.Const1D(5)
    with pytest.raises(TypeError, match=r"Unrecognized projection model type: *"):
        converter.to_yaml_tree_transform(mdl, mk.MagicMock(), mk.MagicMock())

    # from yaml error
    node = {"direction": mk.MagicMock()}
    with pytest.raises(ValueError, match=r"Unrecognized projection direction: *"):
        converter.from_yaml_tree_transform(node, mk.MagicMock(), mk.MagicMock())


def test_polynomial_errors():
    from asdf_astropy.converters.transform.polynomial import PolynomialConverter

    converter = PolynomialConverter()

    # from yaml error
    node = {"coefficients": np.zeros((2, 3))}
    with pytest.raises(TypeError, match=r"Coefficients must be an .* matrix"):
        converter.from_yaml_tree_transform(node, mk.MagicMock(), mk.MagicMock())


def test_compound_errors():
    from asdf_astropy.converters.transform.compound import CompoundConverter

    converter = CompoundConverter()

    # Left not a model
    tag = "!transform/add-1.2.0"
    node = {"forward": [mk.MagicMock(), mk.MagicMock()]}
    with pytest.raises(TypeError, match=r"Unknown left model type '.*'"):
        converter.from_yaml_tree_transform(node, tag, mk.MagicMock())

    # Right not a model (not fix_inputs)
    node = {"forward": [astropy_models.Const1D(17), mk.MagicMock()]}
    with pytest.raises(TypeError, match=r"Unknown right model type '.*'"):
        converter.from_yaml_tree_transform(node, tag, mk.MagicMock())

    # Right not a model (fix_inputs)
    tag = "!transform/fix_inputs-1.2.0"
    mdl = mk.MagicMock()
    mdl.__class__ = astropy_models.Const1D
    node = {"forward": [astropy_models.Const1D(17), mdl]}
    with pytest.raises(TypeError, match=r"Unknown right model type '.*'"):
        converter.from_yaml_tree_transform(node, tag, mk.MagicMock())


def test_bounding_box_missing_attributes():
    yaml = """
model: !transform/constant-1.4.0
    value: 1
    dimensions: 1
    bounding_box: !transform/property/bounding_box-1.0.0
        intervals:
            x: [1.0, 2.0]
    """
    buff = yaml_to_asdf(yaml)
    with asdf.open(buff) as af:
        model = af["model"]
        assert model.bounding_box.ignored == []
        assert model.bounding_box.order == "C"

    yaml = """
model: !transform/constant-1.4.0
    value: 1
    dimensions: 2
    bounding_box: !transform/property/compound_bounding_box-1.0.0
        selector_args:
            - argument: x
              ignore: true
        cbbox:
            - key: [0] # value of input x is 0 to select this box
              bbox: !transform/property/bounding_box-1.0.0
                intervals:
                    y: [1.0, 2.0]
            - key: [3] # value of input x is 3 to select this box
              bbox: !transform/property/bounding_box-1.0.0
                intervals:
                    y: [4.0, 5.0]
    """
    buff = yaml_to_asdf(yaml)
    with asdf.open(buff) as af:
        model = af["model"]
        assert model.bounding_box.order == "C"


@pytest.mark.filterwarnings("ignore:Unable to locate schema file for.*")
@pytest.mark.filterwarnings("ignore:.* not recognized, converting to raw Python data structure")
def test_compound_bbox_ignored_error():
    yaml = """
model: !transform/concatenate-1.2.0
  forward:
    - !transform/concatenate-1.2.0
      forward:
        - !transform/shift-1.2.0
          offset: 1.0
        - !transform/shift-1.2.0
          offset: 2.0
    - !transform/shift-1.2.0
      offset: 3.0
  bounding_box: !transform/property/compound_bounding_box-1.0.0
    selector_args:
      - argument: x
        ignore: true
    cbbox:
      - key: [0] # both value of input x is 0
        bbox: !transform/property/bounding_box-1.0.0
          intervals:
            x0: [2.0, 3.0]
      - key: [1] # both value of input x is 1
        bbox: !transform/property/bounding_box-1.0.0
          intervals:
            x0: [6.0, 7.0]
    ignore: [x1]
    """
    buff = yaml_to_asdf(yaml)
    asdf.open(buff)


def test_serialize_bbox(tmp_path):
    mdl = astropy_models.Const2D(3)
    bind_bounding_box(mdl, (1, 2), ignored="y")
    helpers.assert_model_roundtrip(mdl, tmp_path)


def test_serialize_cbbox(tmp_path):
    mdl = astropy_models.Shift(1) & astropy_models.Scale(2) & astropy_models.Identity(1)
    mdl.inputs = ("x", "y", "slit_id")
    bounding_boxes = {
        (0,): ((-0.5, 1047.5), (-0.5, 2047.5)),
        (1,): ((-0.5, 3047.5), (-0.5, 4047.5)),
    }
    bounding_box = CompoundBoundingBox.validate(mdl, bounding_boxes, selector_args=[("slit_id", True)], order="F")
    mdl.bounding_box = bounding_box

    helpers.assert_model_roundtrip(mdl, tmp_path)
