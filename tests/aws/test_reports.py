import datetime
from dateutil.tz import tzutc
import accloudtant.aws.reports


def test_reports(capsys, monkeypatch, ec2_resource, ec2_client, process_ec2):
    instances = {
        'instances': [{
            'id': 'i-912a4392',
            'tags': [{
                'Key': 'Name',
                'Value': 'web1',
            }, ],
            'instance_type': 'c3.8xlarge',
            'placement': {
                'AvailabilityZone': 'us-east-1c',
            },
            'state': {
                'Name': 'running',
            },
            'launch_time': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc(),
                ),
            'console_output': {'Output': 'Windows', },
        }, {
            'id': 'i-1840273e',
            'tags': [{
                'Key': 'Name',
                'Value': 'app1',
            }, ],
            'instance_type': 'r2.8xlarge',
            'placement': {
                'AvailabilityZone': 'us-east-1b',
            },
            'state': {
                'Name': 'running',
            },
            'launch_time': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc()
                ),
            'console_output': {'Output': 'RHEL Linux', },
        }, {
            'id': 'i-9840273d',
            'tags': [{
                'Key': 'Name',
                'Value': 'app2',
            }, ],
            'instance_type': 'r2.8xlarge',
            'placement': {
                'AvailabilityZone': 'us-east-1c',
            },
            'state': {
                'Name': 'running',
            },
            'launch_time': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc()
                ),
            'console_output': {'Output': 'SUSE Linux', },
        }, {
            'id': 'i-1840273d',
            'tags': [{
                'Key': 'Name',
                'Value': 'database1',
            }, ],
            'instance_type': 'r2.8xlarge',
            'placement': {
                'AvailabilityZone': 'us-east-1c',
            },
            'state': {
                'Name': 'stopped',
            },
            'launch_time': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc()
                ),
            'console_output': {'Output': 'Linux', },
        }, {
            'id': 'i-1840273c',
            'tags': [{
                'Key': 'Name',
                'Value': 'database2',
            }, ],
            'instance_type': 'r2.8xlarge',
            'placement': {
                'AvailabilityZone': 'us-east-1c',
            },
            'state': {
                'Name': 'running',
            },
            'launch_time': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc()
                ),
            'console_output': {'Output': 'Linux', },
        }, {
            'id': 'i-1840273b',
            'tags': [{
                'Key': 'Name',
                'Value': 'database3',
            }, ],
            'instance_type': 'r2.8xlarge',
            'placement': {
                'AvailabilityZone': 'us-east-1c',
            },
            'state': {
                'Name': 'running',
            },
            'launch_time': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc()
                ),
            'console_output': {'Output': 'Linux', },
        }, {
            'id': 'i-912a4393',
            'tags': [{
                'Key': 'Name',
                'Value': 'test',
            }, ],
            'instance_type': 't1.micro',
            'placement': {
                'AvailabilityZone': 'us-east-1c',
            },
            'state': {
                'Name': 'running',
            },
            'launch_time': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc(),
                ),
            'console_output': {'Output': 'Linux', },
        }, ]
    }
    reserved_instances = {
        'ReservedInstances': [{
            'ProductDescription': 'Linux/UNIX',
            'InstanceTenancy': 'default',
            'InstanceCount': 29,
            'InstanceType': 'm1.large',
            'Start': datetime.datetime(
                    2011,
                    6,
                    5,
                    6,
                    20,
                    10,
                    494000,
                    tzinfo=tzutc()
                ),
            'RecurringCharges': [],
            'End': datetime.datetime(
                    2011,
                    6,
                    5,
                    6,
                    20,
                    10,
                    tzinfo=tzutc()
                ),
            'CurrencyCode': 'USD',
            'OfferingType': 'Medium Utilization',
            'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df1223331f',
            'FixedPrice': 910.0,
            'AvailabilityZone': 'us-east-1c',
            'UsagePrice': 0.12,
            'Duration': 31536000,
            'State': 'retired',
        }, {
            'ProductDescription': 'Windows',
            'InstanceTenancy': 'default',
            'InstanceCount': 1,
            'InstanceType': 'c3.8xlarge',
            'Start': datetime.datetime(
                    2015,
                    6,
                    5,
                    6,
                    20,
                    10,
                    494000,
                    tzinfo=tzutc()
                ),
            'RecurringCharges': [],
            'End': datetime.datetime(
                    2016,
                    6,
                    5,
                    6,
                    20,
                    10,
                    494000,
                    tzinfo=tzutc()
                ),
            'CurrencyCode': 'USD',
            'OfferingType': 'Medium Utilization',
            'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df12233320',
            'FixedPrice': 4486.0,
            'AvailabilityZone': 'us-east-1c',
            'UsagePrice': 0.5121,
            'Duration': 31536000,
            'State': 'active',
        }, {
            'ProductDescription': 'Red Hat Enterprise Linux',
            'InstanceTenancy': 'default',
            'InstanceCount': 1,
            'InstanceType': 'r2.8xlarge',
            'Start': datetime.datetime(
                    2015,
                    6,
                    5,
                    6,
                    20,
                    10,
                    494000,
                    tzinfo=tzutc()
                ),
            'RecurringCharges': [],
            'End': datetime.datetime(
                    2016,
                    6,
                    5,
                    6,
                    20,
                    10,
                    494000,
                    tzinfo=tzutc()
                ),
            'CurrencyCode': 'USD',
            'OfferingType': 'Medium Utilization',
            'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df12233321',
            'FixedPrice': 10234,
            'AvailabilityZone': 'us-east-1b',
            'UsagePrice': 0.3894,
            'Duration': 94608000,
            'State': 'active',
        }, {
            'ProductDescription': 'SUSE Linux',
            'InstanceTenancy': 'default',
            'InstanceCount': 1,
            'InstanceType': 'r2.8xlarge',
            'Start': datetime.datetime(
                    2015,
                    6,
                    5,
                    6,
                    20,
                    10,
                    494000,
                    tzinfo=tzutc()
                ),
            'RecurringCharges': [],
            'End': datetime.datetime(
                    2016,
                    6,
                    5,
                    6,
                    20,
                    10,
                    tzinfo=tzutc()
                ),
            'CurrencyCode': 'USD',
            'OfferingType': 'Medium Utilization',
            'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df12233322',
            'FixedPrice': 2974.0,
            'AvailabilityZone': 'us-east-1c',
            'UsagePrice': 0.5225,
            'Duration': 31536000,
            'State': 'active',
        }, {
            'ProductDescription': 'Linux/UNIX',
            'InstanceTenancy': 'default',
            'InstanceCount': 1,
            'InstanceType': 'r2.8xlarge',
            'Start': datetime.datetime(
                    2015,
                    6,
                    5,
                    6,
                    20,
                    10,
                    494000,
                    tzinfo=tzutc()
                ),
            'RecurringCharges': [],
            'End': datetime.datetime(
                    2016,
                    6,
                    5,
                    6,
                    20,
                    10,
                    tzinfo=tzutc()
                ),
            'CurrencyCode': 'USD',
            'OfferingType': 'Medium Utilization',
            'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df12233320',
            'FixedPrice': 5352.36,
            'AvailabilityZone': 'us-east-1c',
            'UsagePrice': 0.611,
            'Duration': 31536000,
            'State': 'active',
        }, {
            'ProductDescription': 'Linux/UNIX',
            'InstanceTenancy': 'default',
            'InstanceCount': 1,
            'InstanceType': 'r2.8xlarge',
            'Start': datetime.datetime(
                    2011,
                    6,
                    5,
                    6,
                    20,
                    10,
                    494000,
                    tzinfo=tzutc()
                ),
            'RecurringCharges': [],
            'End': datetime.datetime(
                    2011,
                    6,
                    5,
                    6,
                    20,
                    10,
                    tzinfo=tzutc()
                ),
            'CurrencyCode': 'USD',
            'OfferingType': 'Medium Utilization',
            'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df12233320',
            'FixedPrice': 5352.36,
            'AvailabilityZone': 'us-east-1c',
            'UsagePrice': 0.611,
            'Duration': 31536000,
            'State': 'active',
        }, ]
    }
    prices = {
        'win': {
            'us-east-1': {
                'c3.8xlarge': {
                    'storageGB': '60 SSD',
                    'ri': {
                        'yrTerm1': {
                            'noUpfront': {
                                'upfront': '0',
                                'monthlyStar': '446.03',
                                'effectiveHourly': '0.611',
                            },
                            'partialUpfront': {
                                'upfront': '2974',
                                'monthlyStar': '133.59',
                                'effectiveHourly': '0.5225',
                            },
                            'allUpfront': {
                                'upfront': '4398.4',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.5021',
                            },
                        },
                        'yrTerm3': {
                            'allUpfront': {
                                'upfront': '10234',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.3894',
                            },
                            'partialUpfront': {
                                'upfront': '7077',
                                'monthlyStar': '105.85',
                                'effectiveHourly': '0.4143',
                            },
                        },
                    },
                    'od': '0.767',
                    'memoryGiB': '15',
                    'vCPU': '8',
                },
            },
        },
        'rhel': {
            'us-east-1': {
                'r2.8xlarge': {
                    'storageGB': '60 SSD',
                    'ri': {
                        'yrTerm1': {
                            'noUpfront': {
                                'upfront': '0',
                                'monthlyStar': '446.03',
                                'effectiveHourly': '0.611',
                            },
                            'partialUpfront': {
                                'upfront': '2974',
                                'monthlyStar': '133.59',
                                'effectiveHourly': '0.5225',
                            },
                            'allUpfront': {
                                'upfront': '4486',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.5121',
                            },
                        },
                        'yrTerm3': {
                            'allUpfront': {
                                'upfront': '10233.432',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.3894',
                            },
                            'partialUpfront': {
                                'upfront': '7077',
                                'monthlyStar': '105.85',
                                'effectiveHourly': '0.4143',
                            },
                        },
                    },
                    'od': '0.767',
                    'memoryGiB': '15',
                    'vCPU': '8',
                },
            },
        },
        'suse': {
            'us-east-1': {
                'r2.8xlarge': {
                    'storageGB': '60 SSD',
                    'ri': {
                        'yrTerm1': {
                            'noUpfront': {
                                'upfront': '0',
                                'monthlyStar': '446.03',
                                'effectiveHourly': '0.611',
                            },
                            'partialUpfront': {
                                'upfront': '2974',
                                'monthlyStar': '133.59',
                                'effectiveHourly': '0.5225',
                            },
                            'allUpfront': {
                                'upfront': '4486',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.5121',
                            },
                        },
                        'yrTerm3': {
                            'allUpfront': {
                                'upfront': '10234',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.3894',
                            },
                            'partialUpfront': {
                                'upfront': '7077',
                                'monthlyStar': '105.85',
                                'effectiveHourly': '0.4143',
                            },
                        },
                    },
                    'od': '0.767',
                    'memoryGiB': '15',
                    'vCPU': '8',
                },
            },
        },
        'linux': {
            'us-east-1': {
                't1.micro': {
                    'storageGB': '60 SSD',
                    'ri': {
                        'yrTerm1': {
                            'noUpfront': {
                                'upfront': '0',
                                'monthlyStar': '446.03',
                                'effectiveHourly': '0.611',
                            },
                            'allUpfront': {
                                'upfront': '2974',
                                'monthlyStar': '133.59',
                                'effectiveHourly': '0.5225',
                            },
                            'partialUpfront': {
                                'upfront': '4486',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.5121',
                            },
                        },
                        'yrTerm3': {
                            'allUpfront': {
                                'upfront': '10234',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.3894',
                            },
                            'partialUpfront': {
                                'upfront': '7077',
                                'monthlyStar': '105.85',
                                'effectiveHourly': '0.4143',
                            },
                        },
                    },
                    'od': '0.767',
                    'memoryGiB': '15',
                    'vCPU': '8',
                },
                'r2.8xlarge': {
                    'storageGB': '60 SSD',
                    'ri': {
                        'yrTerm1': {
                            'noUpfront': {
                                'upfront': '0',
                                'monthlyStar': '446.03',
                                'effectiveHourly': '0.611',
                            },
                            'allUpfront': {
                                'upfront': '2974',
                                'monthlyStar': '133.59',
                                'effectiveHourly': '0.5225',
                            },
                            'partialUpfront': {
                                'upfront': '4486',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.5121',
                            },
                        },
                        'yrTerm3': {
                            'allUpfront': {
                                'upfront': '10234',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.3894',
                            },
                            'partialUpfront': {
                                'upfront': '7077',
                                'monthlyStar': '105.85',
                                'effectiveHourly': '0.4143',
                            },
                        },
                    },
                    'od': '0.767',
                    'memoryGiB': '15',
                    'vCPU': '8',
                },
            },
        },
    }
    expected = open('tests/aws/report_expected.txt', 'r').read()

    monkeypatch.setattr('boto3.resource', ec2_resource)
    ec2_resource.set_responses(instances)
    monkeypatch.setattr('boto3.client', ec2_client)
    ec2_client.set_responses({}, reserved_instances)
    monkeypatch.setattr(
        'accloudtant.aws.prices.process_ec2',
        process_ec2
        )
    process_ec2.set_responses(prices)

    reports = accloudtant.aws.reports.Reports()
    print(reports)
    out, err = capsys.readouterr()

    for mock in instances['instances']:
        assert([True for i in reports.instances if i.id == mock['id']])
    print(out)
    assert(out == expected)
