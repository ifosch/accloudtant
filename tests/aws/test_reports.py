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


def test_reports(capsys, monkeypatch, mock_ec2_resource):
    responses = {
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
        }, ]
    }
    expected = open('tests/aws/report_expected.txt', 'r').read()

    monkeypatch.setattr('boto3.resource', mock_ec2_resource)
    mock_ec2_resource.set_responses(responses)

    reports = accloudtant.aws.reports.Reports()
    print(reports)
    out, err = capsys.readouterr()

    for mock in responses['instances']:
        assert([True for reported in reports.instances if reported == mock])
    print(out)
    assert (out == expected)
