import pytest
import accloudtant.aws.reports


@pytest.fixture
def mock_ec2_resource():
    class MockEC2Instances(object):
        def __init__(self, instances):
            self.instances = instances

        def all(self):
            for instance in self.instances:
                yield instance

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


def test_reports(monkeypatch, mock_ec2_resource):
    responses = {
        'instances': [{
            'id': 'i-31a4r567'
        }, {
            'id': 'i-9e1p3423'
        }]
    }

    monkeypatch.setattr('boto3.resource', mock_ec2_resource)
    mock_ec2_resource.set_responses(responses)

    reports = accloudtant.aws.reports.Reports()

    assert (reports.instances == responses['instances'])
