import asdf
import astropy.units as u
import pytest
from astropy.coordinates import Angle, representation
from numpy.random import default_rng

from asdf_astropy.testing.helpers import assert_representation_equal

IGNORED_REPRESENTATION_CLASSES = [
    "WGS84GeodeticRepresentation",
    "WGS72GeodeticRepresentation",
    "GRS80GeodeticRepresentation",
]

REPRESENTATION_CLASSES = [
    getattr(representation, class_name)
    for class_name in representation.__all__
    if "Base" not in class_name and class_name not in IGNORED_REPRESENTATION_CLASSES
]


def create_representation(rep_class):
    rng = default_rng(42)
    kwargs = {}
    for attr_name, attr_type in rep_class.attr_classes.items():
        value = rng.random((100,)) * u.deg if issubclass(attr_type, Angle) else rng.random((100,)) * u.km
        kwargs[attr_name] = value

    return rep_class(**kwargs)


@pytest.mark.parametrize("rep_class", REPRESENTATION_CLASSES)
def test_serialization(rep_class, tmp_path):
    rep = create_representation(rep_class)
    file_path = tmp_path / "test.asdf"

    with asdf.AsdfFile() as af:
        af["rep"] = rep
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert_representation_equal(af["rep"], rep)
