"""
This module builds all of the ASDF extensions which will be registered by `asdf_astropy.integration`,
via an ``entry-point`` in the ``pyproject.toml`` file.
"""

from asdf.extension import ManifestExtension
from astropy.utils import minversion

from ._manifest import CompoundManifestExtension
from .converters.coordinates.angle import AngleConverter, LatitudeConverter, LongitudeConverter
from .converters.coordinates.earth_location import EarthLocationConverter
from .converters.coordinates.frame import FrameConverter, LegacyICRSConverter
from .converters.coordinates.representation import RepresentationConverter
from .converters.coordinates.sky_coord import SkyCoordConverter
from .converters.coordinates.spectral_coord import SpectralCoordConverter
from .converters.fits.fits import AsdfFitsConverter, AstropyFitsConverter
from .converters.table.table import AsdfTableConverter, AstropyTableConverter, ColumnConverter
from .converters.time.time import TimeConverter
from .converters.time.time_delta import TimeDeltaConverter
from .converters.transform.compound import CompoundConverter
from .converters.transform.core import SimpleTransformConverter
from .converters.transform.functional_models import ConstantConverter
from .converters.transform.mappings import IdentityConverter, RemapAxesConverter, UnitsMappingConverter
from .converters.transform.math_functions import MathFunctionsConverter
from .converters.transform.polynomial import OrthoPolynomialConverter, PolynomialConverter
from .converters.transform.projections import ProjectionConverter
from .converters.transform.properties import CompoundBoundingBoxConverter, ModelBoundingBoxConverter
from .converters.transform.rotations import Rotate3DConverter, RotationSequenceConverter
from .converters.transform.spline import SplineConverter
from .converters.transform.tabular import TabularConverter
from .converters.unit.equivalency import EquivalencyConverter
from .converters.unit.magunit import MagUnitConverter
from .converters.unit.quantity import QuantityConverter
from .converters.unit.unit import UnitConverter

__all__ = [
    "TRANSFORM_CONVERTERS",
    "TRANSFORM_MANIFEST_URIS",
    "TRANSFORM_EXTENSIONS",
    "COORDINATES_CONVERTERS",
    "ASTROPY_CONVERTERS",
    "COORDINATES_EXTENSION",
    "ASTROPY_EXTENSION",
    "CORE_CONVERTERS",
    "CORE_MANIFEST_URIS",
    "CORE_EXTENSIONS",
]

TRANSFORM_CONVERTERS = [
    # astropy.modeling.core
    CompoundConverter(),
    # astropy.modeling.functional_models
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/airy_disk2d-*"],
        "astropy.modeling.functional_models.AiryDisk2D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/box1d-*"],
        "astropy.modeling.functional_models.Box1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/box2d-*"],
        "astropy.modeling.functional_models.Box2D",
    ),
    ConstantConverter(),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/disk2d-*"],
        "astropy.modeling.functional_models.Disk2D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/ellipse2d-*"],
        "astropy.modeling.functional_models.Ellipse2D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/exponential1d-*"],
        "astropy.modeling.functional_models.Exponential1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/gaussian1d-*"],
        "astropy.modeling.functional_models.Gaussian1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/gaussian2d-*"],
        "astropy.modeling.functional_models.Gaussian2D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/king_projected_analytic1d-*"],
        "astropy.modeling.functional_models.KingProjectedAnalytic1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/linear1d-*"],
        "astropy.modeling.functional_models.Linear1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/logarithmic1d-*"],
        "astropy.modeling.functional_models.Logarithmic1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/lorentz1d-*"],
        "astropy.modeling.functional_models.Lorentz1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/moffat1d-*"],
        "astropy.modeling.functional_models.Moffat1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/moffat2d-*"],
        "astropy.modeling.functional_models.Moffat2D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/multiplyscale-*"],
        "astropy.modeling.functional_models.Multiply",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/planar2d-*"],
        "astropy.modeling.functional_models.Planar2D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/redshift_scale_factor-*"],
        "astropy.modeling.functional_models.RedshiftScaleFactor",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/ricker_wavelet1d-*"],
        "astropy.modeling.functional_models.RickerWavelet1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/ricker_wavelet2d-*"],
        "astropy.modeling.functional_models.RickerWavelet2D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/ring2d-*"],
        "astropy.modeling.functional_models.Ring2D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/scale-*"],
        "astropy.modeling.functional_models.Scale",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/sersic1d-*"],
        "astropy.modeling.functional_models.Sersic1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/sersic2d-*"],
        "astropy.modeling.functional_models.Sersic2D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/shift-*"],
        "astropy.modeling.functional_models.Shift",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/sine1d-*"],
        "astropy.modeling.functional_models.Sine1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/cosine1d-*"],
        "astropy.modeling.functional_models.Cosine1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/tangent1d-*"],
        "astropy.modeling.functional_models.Tangent1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/arcsine1d-*"],
        "astropy.modeling.functional_models.ArcSine1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/arccosine1d-*"],
        "astropy.modeling.functional_models.ArcCosine1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/arctangent1d-*"],
        "astropy.modeling.functional_models.ArcTangent1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/trapezoid1d-*"],
        "astropy.modeling.functional_models.Trapezoid1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/trapezoid_disk2d-*"],
        "astropy.modeling.functional_models.TrapezoidDisk2D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/voigt1d-*"],
        "astropy.modeling.functional_models.Voigt1D",
    ),
    # astropy.modeling.mappings
    IdentityConverter(),
    RemapAxesConverter(),
    # UnitsMapping is not represented here because
    # it is an astropy-specific transform and not
    # included in the ASDF transform extension.
    # astropy.modeling.math_functions
    MathFunctionsConverter(),
    # astropy.modeling.physical_models
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/blackbody-*"],
        "astropy.modeling.physical_models.BlackBody",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/drude1d-*"],
        "astropy.modeling.physical_models.Drude1D",
    ),
    # TODO: Implement NFW
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/plummer1d-*"],
        "astropy.modeling.physical_models.Plummer1D",
    ),
    # astropy.modeling.polynomial
    PolynomialConverter(),
    OrthoPolynomialConverter(),
    # SIP and InverseSIP are deliberately excluded because they
    # are FITS-specific and can be easily represented by a
    # simple combination of existing models.
    SplineConverter(),
    # astropy.modeling.powerlaws
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/broken_power_law1d-*"],
        "astropy.modeling.powerlaws.BrokenPowerLaw1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/exponential_cutoff_power_law1d-*"],
        "astropy.modeling.powerlaws.ExponentialCutoffPowerLaw1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/log_parabola1d-*"],
        "astropy.modeling.powerlaws.LogParabola1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/power_law1d-*"],
        "astropy.modeling.powerlaws.PowerLaw1D",
    ),
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/smoothly_broken_power_law1d-*"],
        "astropy.modeling.powerlaws.SmoothlyBrokenPowerLaw1D",
    ),
    # astropy.modeling.projections
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/affine-*"],
        "astropy.modeling.projections.AffineTransformation2D",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/airy-*"],
        "astropy.modeling.projections.Pix2Sky_Airy",
        "astropy.modeling.projections.Sky2Pix_Airy",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/bonne_equal_area-*"],
        "astropy.modeling.projections.Pix2Sky_BonneEqualArea",
        "astropy.modeling.projections.Sky2Pix_BonneEqualArea",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/cobe_quad_spherical_cube-*"],
        "astropy.modeling.projections.Pix2Sky_COBEQuadSphericalCube",
        "astropy.modeling.projections.Sky2Pix_COBEQuadSphericalCube",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/conic_equal_area-*"],
        "astropy.modeling.projections.Pix2Sky_ConicEqualArea",
        "astropy.modeling.projections.Sky2Pix_ConicEqualArea",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/conic_equidistant-*"],
        "astropy.modeling.projections.Pix2Sky_ConicEquidistant",
        "astropy.modeling.projections.Sky2Pix_ConicEquidistant",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/conic_orthomorphic-*"],
        "astropy.modeling.projections.Pix2Sky_ConicOrthomorphic",
        "astropy.modeling.projections.Sky2Pix_ConicOrthomorphic",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/conic_perspective-*"],
        "astropy.modeling.projections.Pix2Sky_ConicPerspective",
        "astropy.modeling.projections.Sky2Pix_ConicPerspective",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/cylindrical_equal_area-*"],
        "astropy.modeling.projections.Pix2Sky_CylindricalEqualArea",
        "astropy.modeling.projections.Sky2Pix_CylindricalEqualArea",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/cylindrical_perspective-*"],
        "astropy.modeling.projections.Pix2Sky_CylindricalPerspective",
        "astropy.modeling.projections.Sky2Pix_CylindricalPerspective",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/gnomonic-*"],
        "astropy.modeling.projections.Pix2Sky_Gnomonic",
        "astropy.modeling.projections.Sky2Pix_Gnomonic",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/hammer_aitoff-*"],
        "astropy.modeling.projections.Pix2Sky_HammerAitoff",
        "astropy.modeling.projections.Sky2Pix_HammerAitoff",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/healpix-*"],
        "astropy.modeling.projections.Pix2Sky_HEALPix",
        "astropy.modeling.projections.Sky2Pix_HEALPix",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/healpix_polar-*"],
        "astropy.modeling.projections.Pix2Sky_HEALPixPolar",
        "astropy.modeling.projections.Sky2Pix_HEALPixPolar",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/mercator-*"],
        "astropy.modeling.projections.Pix2Sky_Mercator",
        "astropy.modeling.projections.Sky2Pix_Mercator",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/molleweide-*"],
        "astropy.modeling.projections.Pix2Sky_Molleweide",
        "astropy.modeling.projections.Sky2Pix_Molleweide",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/parabolic-*"],
        "astropy.modeling.projections.Pix2Sky_Parabolic",
        "astropy.modeling.projections.Sky2Pix_Parabolic",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/plate_carree-*"],
        "astropy.modeling.projections.Pix2Sky_PlateCarree",
        "astropy.modeling.projections.Sky2Pix_PlateCarree",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/polyconic-*"],
        "astropy.modeling.projections.Pix2Sky_Polyconic",
        "astropy.modeling.projections.Sky2Pix_Polyconic",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/quad_spherical_cube-*"],
        "astropy.modeling.projections.Pix2Sky_QuadSphericalCube",
        "astropy.modeling.projections.Sky2Pix_QuadSphericalCube",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/sanson_flamsteed-*"],
        "astropy.modeling.projections.Pix2Sky_SansonFlamsteed",
        "astropy.modeling.projections.Sky2Pix_SansonFlamsteed",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/slant_orthographic-*"],
        "astropy.modeling.projections.Pix2Sky_SlantOrthographic",
        "astropy.modeling.projections.Sky2Pix_SlantOrthographic",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/slant_zenithal_perspective-*"],
        "astropy.modeling.projections.Pix2Sky_SlantZenithalPerspective",
        "astropy.modeling.projections.Sky2Pix_SlantZenithalPerspective",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/stereographic-*"],
        "astropy.modeling.projections.Pix2Sky_Stereographic",
        "astropy.modeling.projections.Sky2Pix_Stereographic",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/tangential_spherical_cube-*"],
        "astropy.modeling.projections.Pix2Sky_TangentialSphericalCube",
        "astropy.modeling.projections.Sky2Pix_TangentialSphericalCube",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/zenithal_equal_area-*"],
        "astropy.modeling.projections.Pix2Sky_ZenithalEqualArea",
        "astropy.modeling.projections.Sky2Pix_ZenithalEqualArea",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/zenithal_equidistant-*"],
        "astropy.modeling.projections.Pix2Sky_ZenithalEquidistant",
        "astropy.modeling.projections.Sky2Pix_ZenithalEquidistant",
    ),
    ProjectionConverter(
        ["tag:stsci.edu:asdf/transform/zenithal_perspective-*"],
        "astropy.modeling.projections.Pix2Sky_ZenithalPerspective",
        "astropy.modeling.projections.Sky2Pix_ZenithalPerspective",
    ),
    # astropy.modeling.rotations
    SimpleTransformConverter(
        ["tag:stsci.edu:asdf/transform/rotate2d-*"],
        "astropy.modeling.rotations.Rotation2D",
    ),
    Rotate3DConverter(),
    RotationSequenceConverter(),
    # astropy.modeling.tabular
    TabularConverter(),
    # astropy.modeling.bounding_box
    ModelBoundingBoxConverter(),
    CompoundBoundingBoxConverter(),
]

if minversion("astropy", "5.1.0"):
    TRANSFORM_CONVERTERS.append(
        SimpleTransformConverter(
            ["tag:stsci.edu:asdf/transform/schechter1d-*"],
            "astropy.modeling.powerlaws.Schechter1D",
        ),
    )


# The order here is important; asdf will prefer to use extensions
# that occur earlier in the list.
TRANSFORM_MANIFEST_URIS = [
    "asdf://asdf-format.org/transform/manifests/transform-1.5.0",
    "asdf://asdf-format.org/transform/manifests/transform-1.4.0",
    "asdf://asdf-format.org/transform/manifests/transform-1.3.0",
    "asdf://asdf-format.org/transform/manifests/transform-1.2.0",
    "asdf://asdf-format.org/transform/manifests/transform-1.1.0",
    "asdf://asdf-format.org/transform/manifests/transform-1.0.0",
]


TRANSFORM_EXTENSIONS = [
    ManifestExtension.from_uri(
        uri,
        # This prevents a warning about a missing extension when opening
        # files written by older versions of the asdf library:
        legacy_class_names=["astropy.io.misc.asdf.extension.AstropyAsdfExtension"],
        converters=TRANSFORM_CONVERTERS,
    )
    for uri in TRANSFORM_MANIFEST_URIS
]


COORDINATES_CONVERTERS = [
    FrameConverter(
        "tag:astropy.org:astropy/coordinates/frames/baseframe-*",
        "astropy.coordinates.baseframe.BaseCoordinateFrame",
    ),
    FrameConverter(
        "tag:astropy.org:astropy/coordinates/frames/cirs-*",
        "astropy.coordinates.builtin_frames.cirs.CIRS",
    ),
    FrameConverter(
        "tag:astropy.org:astropy/coordinates/frames/fk4-*",
        "astropy.coordinates.builtin_frames.fk4.FK4",
    ),
    FrameConverter(
        "tag:astropy.org:astropy/coordinates/frames/fk4noeterms-*",
        "astropy.coordinates.builtin_frames.fk4.FK4NoETerms",
    ),
    FrameConverter(
        "tag:astropy.org:astropy/coordinates/frames/fk5-*",
        "astropy.coordinates.builtin_frames.fk5.FK5",
    ),
    FrameConverter(
        "tag:astropy.org:astropy/coordinates/frames/galactic-*",
        "astropy.coordinates.builtin_frames.galactic.Galactic",
    ),
    FrameConverter(
        "tag:astropy.org:astropy/coordinates/frames/galactocentric-*",
        "astropy.coordinates.builtin_frames.galactocentric.Galactocentric",
    ),
    FrameConverter(
        "tag:astropy.org:astropy/coordinates/frames/gcrs-*",
        "astropy.coordinates.builtin_frames.gcrs.GCRS",
    ),
    FrameConverter(
        "tag:astropy.org:astropy/coordinates/frames/icrs-1.1.0",
        "astropy.coordinates.builtin_frames.icrs.ICRS",
    ),
    FrameConverter(
        "tag:astropy.org:astropy/coordinates/frames/itrs-*",
        "astropy.coordinates.builtin_frames.itrs.ITRS",
    ),
    FrameConverter(
        "tag:astropy.org:astropy/coordinates/frames/precessedgeocentric-*",
        "astropy.coordinates.builtin_frames.gcrs.PrecessedGeocentric",
    ),
    LegacyICRSConverter(),
    AngleConverter(),
    LatitudeConverter(),
    LongitudeConverter(),
    EarthLocationConverter(),
    RepresentationConverter(),
    SkyCoordConverter(),
    SpectralCoordConverter(),
]


ASTROPY_CONVERTERS = [
    UnitsMappingConverter(),
    TimeDeltaConverter(),
    AstropyTableConverter(),
    AstropyFitsConverter(),
]


COORDINATES_EXTENSION = ManifestExtension.from_uri(
    "asdf://asdf-format.org/astronomy/coordinates/manifests/coordinates-1.0.0",
    converters=COORDINATES_CONVERTERS,
)


ASTROPY_EXTENSION = ManifestExtension.from_uri(
    "asdf://astropy.org/astropy/manifests/astropy-1.0.0",
    # This prevents a warning about a missing extension when opening
    # files written by older versions of astropy:
    legacy_class_names=["astropy.io.misc.asdf.extension.AstropyExtension"],
    converters=ASTROPY_CONVERTERS,
)

# These tags are part of the ASDF Standard,
# but we want to override serialization here so that users can
# work with nice astropy objects for those entities.

CORE_CONVERTERS = [
    QuantityConverter(),
    TimeConverter(),
    ColumnConverter(),
    AsdfTableConverter(),
    AsdfFitsConverter(),
]

UNIT_CONVETERS = [
    UnitConverter(),
    EquivalencyConverter(),
    MagUnitConverter(),
]


CORE_MANIFEST_URIS = [
    "asdf://asdf-format.org/core/manifests/core-1.0.0",
    "asdf://asdf-format.org/core/manifests/core-1.1.0",
    "asdf://asdf-format.org/core/manifests/core-1.2.0",
    "asdf://asdf-format.org/core/manifests/core-1.3.0",
    "asdf://asdf-format.org/core/manifests/core-1.4.0",
    "asdf://asdf-format.org/core/manifests/core-1.5.0",
    "asdf://asdf-format.org/core/manifests/core-1.6.0",
]


CORE_EXTENSIONS = [
    CompoundManifestExtension(
        [
            ManifestExtension.from_uri(u, converters=CORE_CONVERTERS),
            ManifestExtension.from_uri("asdf://astropy.org/astropy/manifests/units-1.0.0", converters=UNIT_CONVETERS),
        ],
    )
    for u in CORE_MANIFEST_URIS
]
