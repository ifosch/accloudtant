#   Copyright 2015-2016 See CONTRIBUTORS.md file
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import datetime
from dateutil.tz import tzutc
import accloudtant.aws.reports


def get_future_date(years=1):
    return datetime.datetime.now() + datetime.timedelta(years)


def test_reports_table(capsys, monkeypatch, ec2_resource, ec2_client,
                       process_ec2):
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
            'Scope': 'Availability Zone',
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
            'End': get_future_date(),
            'CurrencyCode': 'USD',
            'OfferingType': 'Medium Utilization',
            'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df12233320',
            'FixedPrice': 4486.0,
            'Scope': 'Availability Zone',
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
            'End': get_future_date(),
            'CurrencyCode': 'USD',
            'OfferingType': 'Medium Utilization',
            'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df12233321',
            'FixedPrice': 10234,
            'Scope': 'Availability Zone',
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
            'End': get_future_date(),
            'CurrencyCode': 'USD',
            'OfferingType': 'Medium Utilization',
            'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df12233322',
            'FixedPrice': 2974.0,
            'Scope': 'Availability Zone',
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
            'End': get_future_date(),
            'CurrencyCode': 'USD',
            'OfferingType': 'Medium Utilization',
            'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df12233320',
            'FixedPrice': 5352.36,
            'Scope': 'Availability Zone',
            'AvailabilityZone': 'us-east-1c',
            'UsagePrice': 0.611,
            'Duration': 31536000,
            'State': 'active',
        }, {
            'ProductDescription': 'Linux/UNIX',
            'InstanceTenancy': 'default',
            'InstanceCount': 1,
            'InstanceType': 't2.micro',
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
            'Scope': 'Availability Zone',
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
            'Scope': 'Availability Zone',
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
                        'yrTerm1Standard': {
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
                        'yrTerm3Standard': {
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
                    'od': '0.867',
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
                        'yrTerm1Standard': {
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
                        'yrTerm3Standard': {
                            'allUpfront': {
                                'upfront': '10233.432',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.3794',
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
                        'yrTerm1Standard': {
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
                        'yrTerm3Standard': {
                            'allUpfront': {
                                'upfront': '10234',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.3890',
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
                        'yrTerm1Standard': {
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
                        'yrTerm3Standard': {
                            'allUpfront': {
                                'upfront': '10234',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.3892',
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
                        'yrTerm1Standard': {
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
                        'yrTerm3Standard': {
                            'allUpfront': {
                                'upfront': '10234',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.3790',
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
    instances_prices = {
        'i-912a4392': {
            'current': 0.5121,
            'best': 0.3894,
        },
        'i-1840273e': {
            'current': 0.3894,
            'best': 0.3794,
        },
        'i-9840273d': {
            'current': 0.5225,
            'best': 0.3890,
        },
        'i-1840273d': {
            'current': 0.0,
            'best': 0.3790,
        },
        'i-1840273c': {
            'current': 0.611,
            'best': 0.3790,
        },
        'i-1840273b': {
            'current': 0.611,
            'best': 0.3790,
        },
        'i-912a4393': {
            'current': 0.767,
            'best': 0.3892,
        },
    }
    expected = open('tests/aws/report_running_expected_table.txt', 'r').read()

    monkeypatch.setattr('boto3.resource', ec2_resource)
    ec2_resource.set_responses(instances)
    monkeypatch.setattr('boto3.client', ec2_client)
    ec2_client.set_responses({}, reserved_instances)
    monkeypatch.setattr(
        'accloudtant.aws.prices.process_ec2',
        process_ec2
        )
    process_ec2.set_responses(prices)

    reports = accloudtant.aws.reports.Reports(output_format='table')
    print(reports)
    out, err = capsys.readouterr()

    assert(len(reports.instances) == 6)
    for mock in instances['instances']:
        mock['current'] = instances_prices[mock['id']]['current']
        mock['best'] = instances_prices[mock['id']]['best']
        for instance in reports.instances:
            if instance.id == mock['id']:
                assert(instance.current == mock['current'])
                assert(instance.best == mock['best'])
    assert(out == expected)


def test_reports_csv(
        capsys,
        monkeypatch,
        ec2_resource,
        ec2_client,
        process_ec2,
):
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
            'Scope': 'Availability Zone',
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
            'End': get_future_date(),
            'CurrencyCode': 'USD',
            'OfferingType': 'Medium Utilization',
            'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df12233320',
            'FixedPrice': 4486.0,
            'Scope': 'Availability Zone',
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
            'End': get_future_date(),
            'CurrencyCode': 'USD',
            'OfferingType': 'Medium Utilization',
            'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df12233321',
            'FixedPrice': 10234,
            'Scope': 'Availability Zone',
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
            'End': get_future_date(),
            'CurrencyCode': 'USD',
            'OfferingType': 'Medium Utilization',
            'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df12233322',
            'FixedPrice': 2974.0,
            'Scope': 'Availability Zone',
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
            'End': get_future_date(),
            'CurrencyCode': 'USD',
            'OfferingType': 'Medium Utilization',
            'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df12233320',
            'FixedPrice': 5352.36,
            'Scope': 'Availability Zone',
            'AvailabilityZone': 'us-east-1c',
            'UsagePrice': 0.611,
            'Duration': 31536000,
            'State': 'active',
        }, {
            'ProductDescription': 'Linux/UNIX',
            'InstanceTenancy': 'default',
            'InstanceCount': 1,
            'InstanceType': 't2.micro',
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
            'Scope': 'Availability Zone',
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
            'Scope': 'Availability Zone',
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
                        'yrTerm1Standard': {
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
                        'yrTerm3Standard': {
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
                    'od': '0.867',
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
                        'yrTerm1Standard': {
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
                        'yrTerm3Standard': {
                            'allUpfront': {
                                'upfront': '10233.432',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.3794',
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
                        'yrTerm1Standard': {
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
                        'yrTerm3Standard': {
                            'allUpfront': {
                                'upfront': '10234',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.3890',
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
                        'yrTerm1Standard': {
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
                        'yrTerm3Standard': {
                            'allUpfront': {
                                'upfront': '10234',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.3892',
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
                        'yrTerm1Standard': {
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
                        'yrTerm3Standard': {
                            'allUpfront': {
                                'upfront': '10234',
                                'monthlyStar': '0',
                                'effectiveHourly': '0.3790',
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
    instances_prices = {
        'i-912a4392': {
            'current': 0.5121,
            'best': 0.3894,
        },
        'i-1840273e': {
            'current': 0.3894,
            'best': 0.3794,
        },
        'i-9840273d': {
            'current': 0.5225,
            'best': 0.3890,
        },
        'i-1840273d': {
            'current': 0.0,
            'best': 0.3790,
        },
        'i-1840273c': {
            'current': 0.611,
            'best': 0.3790,
        },
        'i-1840273b': {
            'current': 0.611,
            'best': 0.3790,
        },
        'i-912a4393': {
            'current': 0.767,
            'best': 0.3892,
        },
    }
    expected = open('tests/aws/report_running_expected_csv.txt', 'r').read()

    monkeypatch.setattr('boto3.resource', ec2_resource)
    ec2_resource.set_responses(instances)
    monkeypatch.setattr('boto3.client', ec2_client)
    ec2_client.set_responses({}, reserved_instances)
    monkeypatch.setattr(
        'accloudtant.aws.prices.process_ec2',
        process_ec2
        )
    process_ec2.set_responses(prices)

    reports = accloudtant.aws.reports.Reports(output_format='csv')
    print(reports)
    out, err = capsys.readouterr()

    assert(len(reports.instances) == 6)
    for mock in instances['instances']:
        mock['current'] = instances_prices[mock['id']]['current']
        mock['best'] = instances_prices[mock['id']]['best']
        for instance in reports.instances:
            if instance.id == mock['id']:
                assert(instance.current == mock['current'])
                assert(instance.best == mock['best'])
    assert(out == expected)
