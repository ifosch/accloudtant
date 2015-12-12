import pytest
import accloudtant.aws.reports


@pytest.mark.xfail(raises=NotImplementedError)
def test_reports():

    accloudtant.aws.reports.Reports()
