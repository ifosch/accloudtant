import csv
import pytest

from accloudtant import load_data
from accloudtant.aws import s3, data_transfer


@pytest.mark.parametrize(
    "csv_file, expected",
    [
        (
            "tests/fixtures/2021/03/S3.csv",
            {
                "AmazonS3": {
                    "EU (Frankfurt)": [
                        "EUC1-Requests-Tier1 6.000 Requests",
                        "EUC1-Requests-Tier2 2861.000 Requests",
                        "EUC1-TimedStorage-ByteHrs 3.995 GB-Mo",
                    ],
                },
                "Data Transfer": {
                    "EU (Frankfurt)": [
                        "EUC1-DataTransfer-Out-Bytes 0.000 GB",
                        "EUC1-DataTransfer-In-Bytes 0.010 GB",
                        "EUC1-CloudFront-Out-Bytes 18.446 GB",
                    ],
                },
            },
        ),
    ],
)
def test_usage_records_totals(csv_file, expected):
    usage = load_data(csv_file)

    for service, entries in usage.services():
        assert service in expected
        for area, concepts in entries.totals():
            assert area in expected[service]
            for c, v, u in concepts:
                assert "{} {} {}".format(c, v, u) in expected[service][area]
