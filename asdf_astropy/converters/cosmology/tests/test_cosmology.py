import asdf
import astropy.units as u
import pytest
from astropy import cosmology
from astropy.cosmology import realizations

from asdf_astropy.converters.cosmology.cosmology import _COSMOLOGY_CLASSES

# one instance of every supported class, plus all the built-in realizations
_PARAMS = {"H0": 70, "Om0": 0.3, "Tcmb0": 2.725, "m_nu": [0, 0, 0.06] * u.eV, "Ob0": 0.05}
_EXTRA = {"Ode0": 0.7, "w0": -0.9, "wa": 0.1, "wp": -0.9, "zp": 0.5, "wz": 0.1}


def _instance(name):
    cls = getattr(cosmology, name)
    extra = {k: v for k, v in _EXTRA.items() if k in cls.parameters}
    return cls(**_PARAMS, **extra, name=f"test-{name}", meta={"note": name})


COSMOLOGIES = [_instance(n) for n in _COSMOLOGY_CLASSES] + [getattr(realizations, n) for n in realizations.available]


@pytest.mark.parametrize("cosmo", COSMOLOGIES, ids=lambda c: c.name)
def test_serialization(cosmo, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["cosmo"] = cosmo
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        loaded = af["cosmo"]
        assert type(loaded) is type(cosmo)
        assert loaded == cosmo
        assert loaded.name == cosmo.name
        assert loaded.meta == cosmo.meta


def test_all_classes_supported():
    """Fail if astropy adds a cosmology class this package doesn't serialize."""
    public = {
        name
        for name in cosmology.__all__
        if isinstance(getattr(cosmology, name), type) and issubclass(getattr(cosmology, name), cosmology.FLRW)
    } - {"FLRW"}
    assert public == set(_COSMOLOGY_CLASSES)
