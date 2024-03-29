import pytest

from accloudtant import load_data, load_files


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
                        "Bandwidth 8.388 GB",
                    ],
                    "Global": [
                        "Invalidations 2.000 URL",
                    ],
                    "United States": [
                        "US-Requests-HTTP-Proxy 27.000 Requests",
                        "US-Requests-Tier1 523.000 Requests",
                        "US-Requests-Tier2-HTTPS 1287.000 Requests",
                        "Bandwidth 4.541 GB",
                        "Bandwidth 0.000 GB",
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
        (
            "tests/fixtures/2021/03/SQS.csv",
            {
                "AWSQueueService": {
                    "EU (Frankfurt)": [
                        "EUC1-Requests-Tier1 2.000 Requests",
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
            if len(concepts) > 0:
                assert area in expected[service]
                for c, v, u in concepts:
                    assert "{} {} {}".format(c, v, u) in expected[service][area]


@pytest.mark.parametrize(
    "csv_files, expected",
    [
        (
            [
                "tests/fixtures/2021/03/S3.csv",
            ],
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
            [
                "tests/fixtures/2021/03/CF.csv",
                "tests/fixtures/2021/03/S3.csv",
            ],
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
                "AmazonCloudFront": {
                    "Canada": [
                        "CA-Requests-Tier1 9.000 Requests",
                        "CA-Requests-Tier2-HTTPS 184.000 Requests",
                        "Bandwidth 0.407 GB",
                    ],
                    "Europe": [
                        "EU-Requests-Tier1 5733.000 Requests",
                        "EU-Requests-Tier2-HTTPS 7998.000 Requests",
                        "Bandwidth 8.388 GB",
                    ],
                    "Global": [
                        "Invalidations 2.000 URL",
                    ],
                    "United States": [
                        "US-Requests-HTTP-Proxy 27.000 Requests",
                        "US-Requests-Tier1 523.000 Requests",
                        "US-Requests-Tier2-HTTPS 1287.000 Requests",
                        "Bandwidth 4.541 GB",
                        "Bandwidth 0.000 GB",
                    ],
                },
            },
        ),
    ],
)
def test_load_files(csv_files, expected):
    usage = load_files(csv_files)

    for service, areas in usage.totals():
        assert service in expected
        for area, concepts in areas.items():
            if len(concepts) > -0:
                assert area in expected[service]
                for c, v, u in concepts:
                    assert "{} {} {}".format(c, v, u) in expected[service][area]
