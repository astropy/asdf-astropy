import asdf
import numpy as np
import pytest
from astropy import units as u
from astropy.nddata import StdDevUncertainty, UnknownUncertainty, VarianceUncertainty


def create_uncertainty():
    uncert = np.arange(100).reshape(10, 10)
    uncertainty_stddev_1 = StdDevUncertainty(uncert, unit="m")
    uncertainty_stddev_2 = StdDevUncertainty([2], unit="m")
    uncertainty_unknown_1 = UnknownUncertainty(uncert, unit="m")
    uncertainty_unknown_2 = UnknownUncertainty([0.4], unit=u.adu)
    uncertainty_variance_1 = VarianceUncertainty(uncert, unit="m")
    uncertainty_variance_2 = VarianceUncertainty([0.4], unit=u.adu)
    return [
        uncertainty_stddev_1,
        uncertainty_stddev_2,
        uncertainty_unknown_1,
        uncertainty_unknown_2,
        uncertainty_variance_1,
        uncertainty_variance_2,
    ]


@pytest.mark.parametrize("uncertainty", create_uncertainty())
def test_uncertainty_serialization(uncertainty, tmp_path):
    file_path = tmp_path / "test_uncertainty.asdf"
    with asdf.AsdfFile() as af:
        af["uncertainty"] = uncertainty
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        loaded_uncert = af["uncertainty"]
        assert type(loaded_uncert) is type(uncertainty)
        assert (loaded_uncert._array == uncertainty._array).all()
        assert loaded_uncert.unit == uncertainty.unit
