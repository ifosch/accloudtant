import csv
import pytest

from accloudtant.usage_record import UsageRecord
from accloudtant.usage_records import UsageRecords


@pytest.mark.parametrize(
    "csv_file, omit_lambda, expected",
    [
        (
            "tests/fixtures/2021/03/S3.csv",
            lambda x: x.is_data_transfer or x.type == "StorageObjectCount",
            {
                "EU (Frankfurt)": [
                    "EUC1-Requests-Tier1 6.000 Requests",
                    "EUC1-Requests-Tier2 2861.000 Requests",
                    "EUC1-TimedStorage-ByteHrs 3.995 GB-Mo",
                ],
            },
        ),
    ],
)
def test_usage_records_totals(csv_file, omit_lambda, expected):
    usage = UsageRecords()

    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            usage.append(UsageRecord(row))

    for area, concepts in usage.totals(omit=omit_lambda):
        assert area in expected
        for c, v, u in concepts:
            assert "{} {} {}".format(c, v, u) in expected[area]


@pytest.mark.parametrize(
    "csv_file, omit_lambda, expected",
    [
        (
            "tests/fixtures/2021/03/S3.csv",
            lambda x: not x.is_data_transfer,
            {
                "EU (Frankfurt)": [
                    "EUC1-DataTransfer-Out-Bytes 0.000 GB",
                    "EUC1-DataTransfer-In-Bytes 0.010 GB",
                    "EUC1-CloudFront-Out-Bytes 18.446 GB",
                ],
            },
        ),
    ],
)
def test_usage_records_data_transfers(csv_file, omit_lambda, expected):
    usage = UsageRecords()

    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            usage.append(UsageRecord(row))

    for area, concepts in usage.data_transfers().totals(omit=omit_lambda):
        assert area in expected
        for c, v, u in concepts:
            assert "{} {} {}".format(c, v, u) in expected[area]
