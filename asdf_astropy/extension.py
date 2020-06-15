# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
import asdf

# Make sure that all tag implementations are imported by the time we create
# the extension class so that _astropy_asdf_types is populated correctly. We
# could do this using __init__ files, except it causes pytest import errors in
# the case that asdf is not installed.
'''
from .tags.coordinates.angle import *  # noqa
from .tags.coordinates.frames import *  # noqa
from .tags.coordinates.earthlocation import *  # noqa
from .tags.coordinates.skycoord import *  # noqa
from .tags.coordinates.representation import *  # noqa
from .tags.coordinates.spectralcoord import *  # noqa
from .tags.fits.fits import *  # noqa
from .tags.table.table import *  # noqa
from .tags.time.time import *  # noqa
from .tags.time.timedelta import *  # noqa
'''
from .tags.transform.basic import *  # noqa
from .tags.transform.polynomial import *  # noqa
from .tags.transform.compound import *  # noqa
from .tags.transform.functional_models import *  # noqa
from .tags.transform.physical_models import *  # noqa
from .tags.transform.math import *  # noqa
from .tags.transform.powerlaws import *  # noqa
from .tags.transform.projections import *  # noqa
from .tags.transform.tabular import *  # noqa
'''
from .tags.unit.quantity import *  # noqa
from .tags.unit.unit import *  # noqa
from .tags.unit.equivalency import *  # noqa
'''

_asdf_format_types = {
    AffineConverter, AiryDisk2DConverter, AiryConverter,
    BonneEqualAreaConverter, Box1DConverter, Box2DConverter, BrokenPowerLaw1DConverter,
    COBEQuadSphericalCubeConverter, CompoundConverter, ConicEqualAreaConverter, ConicEquidistantConverter,
    ConicOrthomorphicConverter, ConicPerspectiveConverter,
    CylindricalEqualAreaConverter, CylindricalPerspectiveConverter,
    Disk2DConverter,
    Ellipse2DConverter, Exponential1DConverter, ExponentialCutoffPowerLaw1DConverter,
    Gaussian1DConverter, Gaussian2DConverter, GnomonicConverter,
    HammerAitoffConverter, HEALPixPolarConverter, HEALPixConverter,
    KingProjectedAnalytic1DConverter,
    Linear1DConverter, Logarithmic1DConverter, Lorentz1DConverter, LogParabola1DConverter,
    MercatorConverter, Moffat1DConverter, Moffat2DConverter, MolleweideConverter, MultiplyConverter,
    NpUfuncConverter,
    OrthoPolynomialConverter,
    ParabolicConverter, Planar2D, PlateCarreeConverter, PolyconicConverter, PolynomialConverterBase,
    PowerLaw1DConverter,
    QuadSphericalCubeConverter,
    RedshiftScaleFactorConverter, RemapAxesConverter, RickerWavelet1DConverter, RickerWavelet2DConverter,
    Ring2DConverter, Rotate2DConverter, Rotate3DConverter, RotationSequenceConverter,
    SansonFlamsteedConverter, ScaleConverter, Sersic1DConverter, Sersic2DConverter, ShiftConverter, Sine1DConverter,
    SmoothlyBrokenPowerLaw1DConverter, StereographicConverter, SlantOrthographicConverter,
    TabularConverter, TangentialSphericalCubeConverter, Trapezoid1DConverter, TrapezoidDisk2DConverter,
    Voigt1DConverter,
    ZenithalPerspectiveConverter, ZenithalEquidistantConverter, ZenithalEqualAreaConverter,
    }


__all__ = ['TransformConverterProvider']


class TransformConverterProvider(asdf.AsdfConverterProvider):
    converter_classes = list(_asdf_format_types)
