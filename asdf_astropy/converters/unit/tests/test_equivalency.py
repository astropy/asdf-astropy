import asdf
import astropy
import pytest
from astropy import units as u
from astropy.cosmology import Planck15
from astropy.cosmology.units import with_H0
from astropy.units import equivalencies as eq
from packaging.version import Version


def create_equivalencies():
    result = [
        eq.plate_scale(0.3 * u.deg / u.mm),
        eq.pixel_scale(0.5 * u.deg / u.pix),
        eq.spectral_density(350 * u.nm),
        eq.spectral(),
        eq.brightness_temperature(500 * u.GHz),
        eq.brightness_temperature(500 * u.GHz, beam_area=23 * u.sr),
        with_H0(),
        eq.temperature_energy(),
        eq.temperature(),
        eq.thermodynamic_temperature(300 * u.Hz),
        eq.thermodynamic_temperature(140 * u.GHz, Planck15.Tcmb0),
        eq.beam_angular_area(3 * u.sr),
        eq.mass_energy(),
        eq.molar_mass_amu(),
        eq.doppler_relativistic(2 * u.m),
        eq.doppler_optical(2 * u.nm),
        eq.doppler_radio(2 * u.Hz),
        eq.parallax(),
        eq.logarithmic(),
        eq.dimensionless_angles(),
        eq.spectral() + eq.temperature(),
        (eq.spectral_density(35 * u.nm) + eq.brightness_temperature(5 * u.Hz, beam_area=2 * u.sr)),
        (eq.spectral() + eq.spectral_density(35 * u.nm) + eq.brightness_temperature(5 * u.Hz, beam_area=2 * u.sr)),
    ]

    if Version(astropy.__version__) >= Version("4.1"):
        result.append(eq.pixel_scale(100.0 * u.pix / u.cm))

    # the factor argument to spectral density is deprecated in astropy 7
    # skip this test to avoid test failures due to the deprecation warning
    if Version(astropy.__version__) < Version("7.0.0.dev"):
        result.append(eq.spectral_density(350 * u.nm, factor=2))
    return result


@pytest.mark.parametrize("equivalency", create_equivalencies())
def test_serialization(equivalency, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["equivalency"] = equivalency
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert af["equivalency"] == equivalency
