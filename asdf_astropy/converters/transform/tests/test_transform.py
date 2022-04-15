import itertools

import asdf
import astropy
import astropy.modeling
import numpy as np
import pytest
from asdf.tests.helpers import yaml_to_asdf
from astropy import units as u
from astropy.modeling import models as astropy_models

from asdf_astropy import integration
from asdf_astropy.testing.helpers import assert_model_equal


def assert_model_roundtrip(model, tmpdir, version=None):
    """
    Assert that a model can be written to an ASDF file and read back
    in without losing any of its essential properties.
    """
    path = str(tmpdir / "test.asdf")

    with asdf.AsdfFile({"model": model}, version=version) as af:
        af.write_to(path)

    with asdf.open(path) as af:
        assert_model_equal(model, af["model"])
        return af["model"]


def create_single_models():
    model_with_bounding_box = astropy_models.Shift(10)
    model_with_bounding_box.bounding_box = ((1, 7),)

    model_with_user_inverse = astropy_models.Shift(10)
    model_with_user_inverse.inverse = astropy_models.Shift(-7)

    model_with_constraints = astropy_models.Legendre2D(
        x_degree=1, y_degree=1, c0_0=1, c0_1=2, c1_0=3, fixed={"c1_0": True, "c0_1": True}, bounds={"c0_0": (-10, 10)}
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
                [0.10412331, 0.07013616, -0.18799552, 1.35953147, -0.15282581, 0.03923, -0.04297299, 0.0, 0.0, 0.0, 0.0]
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
            matrix=np.array([[1.0, 2.0], [3.0, 4.0]]), translation=np.array([5.0, 6.0])
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


@pytest.mark.parametrize("model", create_single_models())
def test_single_model(tmpdir, model):
    assert_model_roundtrip(model, tmpdir)


def test_all_models_supported():
    """
    Test that all model classes in astropy have serialization
    support implemented in this package.  If this test fails,
    file an issue on GitHub for each missing model and add
    the model to the UNSUPPORTED_MODELS list above with
    a link to the issue in a comment.
    """

    def _iterate_model_classes():
        for key, value in itertools.chain(
            astropy_models.__dict__.items(), astropy.modeling.math_functions.__dict__.items()
        ):
            if (
                isinstance(value, type)
                and issubclass(value, astropy.modeling.core.Model)
                and value not in UNSUPPORTED_MODELS
            ):
                yield value

    extensions = integration.get_extensions()
    extension_manager = asdf.extension.ExtensionManager(extensions)

    missing = set()
    for model_class in _iterate_model_classes():
        if not extension_manager.handles_type(model_class):
            missing.add(model_class)

    if len(missing) > 0:
        class_names = sorted([f"{m.__module__}.{m.__qualname__}" for m in missing])
        message = "Missing support for the following model classes:\n\n" + "\n".join(class_names)
        assert len(missing) == 0, message


def test_legacy_const(tmpdir):
    with asdf.config_context() as config:
        config.remove_extension("asdf://asdf-format.org/transform/extensions/transform-1.5.0")

        model = astropy_models.Const1D(amplitude=5.0)
        assert_model_roundtrip(model, tmpdir, version="1.3.0")

        model = astropy_models.Const2D(amplitude=5.0)
        with pytest.raises(TypeError, match=r".* does not support models with > 1 dimension"):
            assert_model_roundtrip(model, tmpdir, version="1.3.0")


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
def test_compound_model(tmpdir, operator):
    left_model = astropy_models.Shift(5)
    right_model = astropy_models.Shift(-1)
    model = getattr(left_model, operator)(right_model)
    result = assert_model_roundtrip(model, tmpdir)
    assert_model_equal(result.left, left_model)
    assert_model_equal(result.right, right_model)
    assert result.op == model.op


def test_fix_inputs(tmpdir):
    model = astropy_models.Gaussian2D(1, 2, 3, 4, 5)
    fixed_model = astropy_models.fix_inputs(model, {"x": 2.5})
    result = assert_model_roundtrip(fixed_model, tmpdir)
    assert_model_equal(result.left, model)
    assert result.right == fixed_model.right
    assert result.op == fixed_model.op


def test_units_mapping(tmpdir):
    # Basic mapping between units:
    model = astropy_models.UnitsMapping(((u.m, u.dimensionless_unscaled),))
    model.name = "foo"
    result = assert_model_roundtrip(model, tmpdir)
    assert result.mapping == model.mapping

    # Remove units:
    model = astropy_models.UnitsMapping(((u.m, None),))
    result = assert_model_roundtrip(model, tmpdir)
    assert result.mapping == model.mapping

    # Change a model to accept any units:
    model = astropy_models.UnitsMapping(((None, u.m),))
    result = assert_model_roundtrip(model, tmpdir)
    assert result.mapping == model.mapping

    # With equivalencies:
    model = astropy_models.UnitsMapping(
        ((u.m, u.dimensionless_unscaled),), input_units_equivalencies={"x": u.equivalencies.spectral()}
    )
    result = assert_model_roundtrip(model, tmpdir)
    assert result.mapping == model.mapping

    # Allow dimensionless on all inputs:
    model = astropy_models.UnitsMapping(
        ((u.m, u.dimensionless_unscaled), (u.s, u.Hz)), input_units_allow_dimensionless=True
    )
    result = assert_model_roundtrip(model, tmpdir)
    assert result.mapping == model.mapping

    # Allow dimensionless selectively:
    model = astropy_models.UnitsMapping(
        ((u.m, u.dimensionless_unscaled), (u.s, u.Hz)), input_units_allow_dimensionless={"x0": True, "x1": False}
    )
    result = assert_model_roundtrip(model, tmpdir)
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
def test_1d_polynomial_with_asdf_standard_version(tmpdir, standard_version, model):
    result = assert_model_roundtrip(model, tmpdir, version=standard_version)
    assert result.domain == model.domain
    assert result.window == model.window


@pytest.mark.parametrize("standard_version", [v for v in asdf.versioning.supported_versions if v >= "1.4.0"])
@pytest.mark.parametrize(
    "model",
    [
        astropy_models.Polynomial2D(2, c0_0=3, c1_0=5, c0_1=7),
        astropy_models.Polynomial2D(
            2, c0_0=3, c1_0=5, c0_1=7, x_domain=[-2, 2], y_domain=[-4, 4], x_window=[-6, 6], y_window=[-8, 8]
        ),
        astropy_models.Chebyshev2D(1, 1, c0_0=1, c0_1=2, c1_0=3, x_domain=[-2, 2], y_domain=[-2, 2]),
        astropy_models.Chebyshev2D(
            1, 1, c0_0=1, c0_1=2, c1_0=3, x_domain=[-2, 2], y_domain=[-2, 2], x_window=[-0.5, 0.5], y_window=[-0.1, 0.5]
        ),
    ],
)
def test_2d_polynomial_with_asdf_standard_version(tmpdir, standard_version, model):
    result = assert_model_roundtrip(model, tmpdir, version=standard_version)
    assert result.x_domain == model.x_domain
    assert result.y_domain == model.y_domain
    assert result.x_window == model.x_window
    assert result.y_window == model.y_window


def test_deserialize_compound_user_inverse(tmpdir):
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
