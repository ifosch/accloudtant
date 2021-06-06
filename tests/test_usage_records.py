import csv
import pytest

from accloudtant import load_data


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
        (
            "tests/fixtures/2021/03/CF.csv",
            {
                "AmazonCloudFront": {
                    "Canada": [
                        "CA-Requests-Tier1 9.000 Requests",
                        "CA-Requests-Tier2-HTTPS 184.000 Requests",
                        "Bandwidth 0.407 GB",
                    ],
                    "Europe": [
                        "EU-Requests-Tier1 5733.000 Requests",
                        "EU-Requests-Tier2-HTTPS 7998.000 Requests",
                        "Bandwidth 35.058 GB",
                    ],
                    "Global": [
                        "Invalidations 2.000 URL",
                    ],
                    "United States": [
                        "US-Requests-HTTP-Proxy 27.000 Requests",
                        "US-Requests-Tier1 523.000 Requests",
                        "US-Requests-Tier2-HTTPS 1287.000 Requests",
                        "Bandwidth 4.541 GB",
                    ],
                },
            },
        ),
        (
            "tests/fixtures/2021/03/R53.csv",
            {
                "AmazonRoute53": {
                    "Global": [
                        "HostedZone 1.000 Hosted zones",
                        "DNS-Queries 79465.000 Queries",
                    ],
                },
            },
        ),
    ],
)
def test_usage_records_totals(csv_file, expected):
    usage = load_data(csv_file)

    for service, areas in usage.totals():
        assert service in expected
        for area, concepts in areas.items():
            assert area in expected[service]
            for c, v, u in concepts:
                assert "{} {} {}".format(c, v, u) in expected[service][area]
