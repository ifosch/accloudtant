import datetime
from dateutil.tz import tzutc
import pytest
import accloudtant.aws.reports


@pytest.fixture
def mock_ec2_resource():
    class MockEC2Instance(object):
        def __init__(self, instance):
            self.instance = instance

        def __eq__(self, obj):
            if isinstance(obj, dict):
                return self.id == obj['id']
            else:
                return self.id == obj.id

        def console_output(self):
            return self.instance['console_output']

        @property
        def id(self):
            return self.instance['id']

        @property
        def tags(self):
            return self.instance['tags']

        @property
        def instance_type(self):
            return self.instance['instance_type']

        @property
        def placement(self):
            return self.instance['placement']

        @property
        def state(self):
            return self.instance['state']

        @property
        def launch_time(self):
            return self.instance['launch_time']

    class MockEC2Instances(object):
        def __init__(self, instances):
            self.instances = instances

        def all(self):
            for instance in self.instances:
                yield MockEC2Instance(instance)

    class MockEC2Resource(object):
        def __init__(self, responses):
            self.responses = responses

        def __getattr__(self, name):
            return MockEC2Instances(self.responses['instances'])

    class MockEC2ResourceCall(object):
        def set_responses(self, responses=None):
            if responses is None:
                responses = {}
            self.responses = responses

        def __call__(self, *args):
            return MockEC2Resource(self.responses)

    return MockEC2ResourceCall()


@pytest.fixture
def mock_ec2_client():
    class MockEC2Client(object):
        def __init__(self, responses):
            self.responses = responses

        def describe_instances(self):
            return self.responses

    class MockEC2ClientCall(object):
        def set_responses(self, responses=None):
            if responses is None:
                responses = {}
            self.responses = responses

        def __call__(self, *args):
            return MockEC2Client(self.responses)

    return MockEC2ClientCall()


def test_reports(capsys, monkeypatch, mock_ec2_resource, mock_ec2_client):
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
    arn = 'arn:aws:iam::103656693407:instance-profile/aws-ec2-role'
    reservations = {
        'Reservations': [{
            'Groups': [{
                'GroupId': 'sg-67b3450e',
                'GroupName': 'web-servers',
            }, ],
            'OwnerId': '103656693407',
            'ReservationId': 'r-0623c177',
            'Instances': [{
                'ImageId': 'ami-9ad904f1',
                'AmiLaunchIndex': 0,
                'VirtualizationType': 'paravirtual',
                'RootDeviceType': 'ebs',
                'LaunchTime': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc(),
                ),
                'ProductCodes': [],
                'Architecture': 'x86_64',
                'Monitoring': {
                    'State': 'disabled',
                },
                'PrivateDnsName': 'ip-10-140-171-36.ec2.internal',
                'InstanceId': 'i-912a4392',
                'RootDeviceName': '/dev/sda1',
                'KernelId': 'aki-825eae7b',
                'ClientToken': '88c854ec-a622-41e1-0f9e-11323b21fabe',
                'StateTransitionReason': '',
                'PrivateIpAddress': '10.140.171.36',
                'State': {
                    'Code': 16,
                    'Name': 'running',
                },
                'KeyName': 'keypair',
                'Hypervisor': 'xen',
                'BlockDeviceMappings': [{
                    'Ebs': {
                        'VolumeId': 'vol-f411b440',
                        'Status': 'attached',
                        'AttachTime': datetime.datetime(
                            2015,
                            10,
                            22,
                            14,
                            15,
                            10,
                            tzinfo=tzutc(),
                        ),
                        'DeleteOnTermination': True,
                    },
                    'DeviceName': '/dev/sda1',
                }, ],
                'EbsOptimized': False,
                'IamInstanceProfile': {
                    'Id': 'APIAFIH55CMB52TYXLESR',
                    'Arn': arn,
                },
                'InstanceType': 'c3.8xlarge',
                'Tags': [{
                    'Key': 'Name',
                    'Value': 'web1',
                }, ],
                'NetworkInterfaces': [],
                'Placement': {
                    'AvailabilityZone': 'us-east-1c',
                    'GroupName': '',
                    'Tenancy': 'default',
                },
                'SecurityGroups': [{
                    'GroupId': 'sg-67b3450e',
                    'GroupName': 'web-servers',
                }, ],
                'PublicIpAddress': '174.20.71.129',
                'PublicDnsName': 'ec2-174-20-71-129.compute-1.amazonaws.com',
            }, ],
        }, {
            'Groups': [{
                'GroupId': 'sg-67b3450f',
                'GroupName': 'app-servers',
            }, ],
            'OwnerId': '103656693407',
            'ReservationId': 'r-0717c236',
            'Instances': [{
                'ImageId': 'ami-9ad904f2',
                'AmiLaunchIndex': 0,
                'VirtualizationType': 'paravirtual',
                'RootDeviceType': 'ebs',
                'LaunchTime': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc()
                ),
                'ProductCodes': [],
                'Architecture': 'x86_64',
                'Monitoring': {
                    'State': 'disabled',
                },
                'PrivateDnsName': 'ip-10-10-117-36.ec2.internal',
                'InstanceId': 'i-1840273e',
                'RootDeviceName': '/dev/sda1',
                'KernelId': 'aki-825eae7c',
                'ClientToken': '88c854ec-a622-41e1-0f9e-11323b21befa',
                'StateTransitionReason': '',
                'PrivateIpAddress': '10.10.117.36',
                'State': {
                    'Code': 16,
                    'Name': 'running',
                },
                'KeyName': 'keypair',
                'Hypervisor': 'xen',
                'BlockDeviceMappings': [{
                    'Ebs': {
                        'VolumeId': 'vol-f411b441',
                        'Status': 'attached',
                        'AttachTime': datetime.datetime(
                            2015,
                            10,
                            22,
                            14,
                            15,
                            10,
                            tzinfo=tzutc(),
                        ),
                        'DeleteOnTermination': True,
                    },
                    'DeviceName': '/dev/sda1',
                }, ],
                'EbsOptimized': False,
                'IamInstanceProfile': {
                    'Id': 'APIAFIH55CMB52TYXLESR',
                    'Arn': arn,
                },
                'InstanceType': 'r2.8xlarge',
                'Tags': [{
                    'Key': 'Name',
                    'Value': 'app1',
                }, ],
                'NetworkInterfaces': [],
                'Placement': {
                    'AvailabilityZone': 'us-east-1b',
                    'GroupName': '',
                    'Tenancy': 'default',
                },
                'SecurityGroups': [{
                    'GroupId': 'sg-67b3450f',
                    'GroupName': 'app-servers',
                }, ],
                'PublicIpAddress': '174.40.71.129',
                'PublicDnsName': 'ec2-174-40-71-129.compute-1.amazonaws.com',
            }, ],
        }, {
            'Groups': [{
                'GroupId': 'sg-67b3450f',
                'GroupName': 'app-servers',
            }, ],
            'OwnerId': '103656693407',
            'ReservationId': 'r-23076c17',
            'Instances': [{
                'ImageId': 'ami-9ad904f3',
                'AmiLaunchIndex': 0,
                'VirtualizationType': 'paravirtual',
                'RootDeviceType': 'ebs',
                'LaunchTime': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc()
                ),
                'ProductCodes': [],
                'Architecture': 'x86_64',
                'Monitoring': {
                    'State': 'disabled',
                },
                'PrivateDnsName': 'ip-10-36-117-10.ec2.internal',
                'InstanceId': 'i-9840273d',
                'RootDeviceName': '/dev/sda1',
                'KernelId': 'aki-825eae7d',
                'ClientToken': '88c854ec-a622-41e1-0f9e-11323b21befa',
                'StateTransitionReason': '',
                'PrivateIpAddress': '10.36.117.10',
                'State': {
                    'Code': 80,
                    'Name': 'stopped',
                },
                'KeyName': 'keypair',
                'Hypervisor': 'xen',
                'BlockDeviceMappings': [{
                    'Ebs': {
                        'VolumeId': 'vol-411f441b',
                        'Status': 'attached',
                        'AttachTime': datetime.datetime(
                            2015,
                            10,
                            22,
                            14,
                            15,
                            10,
                            tzinfo=tzutc(),
                        ),
                        'DeleteOnTermination': True,
                    },
                    'DeviceName': '/dev/sda1',
                }, ],
                'EbsOptimized': False,
                'IamInstanceProfile': {
                    'Id': 'APIAFIH55CMB52TYXLESR',
                    'Arn': arn,
                },
                'InstanceType': 'r2.8xlarge',
                'Tags': [{
                    'Key': 'Name',
                    'Value': 'app2',
                }, ],
                'NetworkInterfaces': [],
                'Placement': {
                    'AvailabilityZone': 'us-east-1c',
                    'GroupName': '',
                    'Tenancy': 'default',
                },
                'SecurityGroups': [{
                    'GroupId': 'sg-67b3450f',
                    'GroupName': 'app-servers',
                }, ],
                'PublicIpAddress': '171.40.74.129',
                'PublicDnsName': 'ec2-171-40-74-129.compute-1.amazonaws.com',
            }, ],
        }, {
            'Groups': [{
                'GroupId': 'sg-67b34510',
                'GroupName': 'db-servers',
            }, ],
            'OwnerId': '103656693407',
            'ReservationId': 'r-0717c237',
            'Instances': [{
                'ImageId': 'ami-9ad904f3',
                'AmiLaunchIndex': 0,
                'VirtualizationType': 'paravirtual',
                'RootDeviceType': 'ebs',
                'LaunchTime': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc()
                ),
                'ProductCodes': [],
                'Architecture': 'x86_64',
                'Monitoring': {
                    'State': 'disabled',
                },
                'PrivateDnsName': 'ip-10-17-136-10.ec2.internal',
                'InstanceId': 'i-1840273d',
                'RootDeviceName': '/dev/sda1',
                'KernelId': 'aki-825eae7d',
                'ClientToken': '88c854ec-a622-41e1-0f9e-11323b21befa',
                'StateTransitionReason': '',
                'PrivateIpAddress': '10.17.136.10',
                'State': {
                    'Code': 80,
                    'Name': 'stopped',
                },
                'KeyName': 'keypair',
                'Hypervisor': 'xen',
                'BlockDeviceMappings': [{
                    'Ebs': {
                        'VolumeId': 'vol-f411b443',
                        'Status': 'attached',
                        'AttachTime': datetime.datetime(
                            2015,
                            10,
                            22,
                            14,
                            15,
                            10,
                            tzinfo=tzutc(),
                        ),
                        'DeleteOnTermination': True,
                    },
                    'DeviceName': '/dev/sda1',
                }, ],
                'EbsOptimized': False,
                'IamInstanceProfile': {
                    'Id': 'APIAFIH55CMB52TYXLESR',
                    'Arn': arn,
                },
                'InstanceType': 'r2.8xlarge',
                'Tags': [{
                    'Key': 'Name',
                    'Value': 'database1',
                }, ],
                'NetworkInterfaces': [],
                'Placement': {
                    'AvailabilityZone': 'us-east-1c',
                    'GroupName': '',
                    'Tenancy': 'default',
                },
                'SecurityGroups': [{
                    'GroupId': 'sg-67b34510',
                    'GroupName': 'db-servers',
                }, ],
                'PublicIpAddress': '129.40.71.174',
                'PublicDnsName': 'ec2-129-40-71-174.compute-1.amazonaws.com',
            }, {
                'ImageId': 'ami-9ad904f3',
                'AmiLaunchIndex': 0,
                'VirtualizationType': 'paravirtual',
                'RootDeviceType': 'ebs',
                'LaunchTime': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc()
                ),
                'ProductCodes': [],
                'Architecture': 'x86_64',
                'Monitoring': {
                    'State': 'disabled',
                },
                'PrivateDnsName': 'ip-10-17-136-11.ec2.internal',
                'InstanceId': 'i-1840273c',
                'RootDeviceName': '/dev/sda1',
                'KernelId': 'aki-825eae7d',
                'ClientToken': '88c854ec-a622-41e1-0f9e-11323b21befa',
                'StateTransitionReason': '',
                'PrivateIpAddress': '10.17.136.11',
                'State': {
                    'Code': 16,
                    'Name': 'running',
                },
                'KeyName': 'keypair',
                'Hypervisor': 'xen',
                'BlockDeviceMappings': [{
                    'Ebs': {
                        'VolumeId': 'vol-f411b444',
                        'Status': 'attached',
                        'AttachTime': datetime.datetime(
                            2015,
                            10,
                            22,
                            14,
                            15,
                            10,
                            tzinfo=tzutc(),
                        ),
                        'DeleteOnTermination': True,
                    },
                    'DeviceName': '/dev/sda1',
                }, ],
                'EbsOptimized': False,
                'IamInstanceProfile': {
                    'Id': 'APIAFIH55CMB52TYXLESR',
                    'Arn': arn,
                },
                'InstanceType': 'r2.8xlarge',
                'Tags': [{
                    'Key': 'Name',
                    'Value': 'database2',
                }, ],
                'NetworkInterfaces': [],
                'Placement': {
                    'AvailabilityZone': 'us-east-1c',
                    'GroupName': '',
                    'Tenancy': 'default',
                },
                'SecurityGroups': [{
                    'GroupId': 'sg-67b34510',
                    'GroupName': 'db-servers',
                }, ],
                'PublicIpAddress': '129.40.71.175',
                'PublicDnsName': 'ec2-129-40-71-175.compute-1.amazonaws.com',
            }, ],
        }, ]
    }
    expected = open('tests/aws/report_expected.txt', 'r').read()

    monkeypatch.setattr('boto3.resource', mock_ec2_resource)
    mock_ec2_resource.set_responses(instances)
    monkeypatch.setattr('boto3.client', mock_ec2_client)
    mock_ec2_client.set_responses(reservations)

    reports = accloudtant.aws.reports.Reports()
    print(reports)
    out, err = capsys.readouterr()

    for mock in instances['instances']:
        assert([True for reported in reports.instances if reported == mock])
    print(out)
    assert (out == expected)
