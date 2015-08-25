import pytest
from accloudtant.prices.aws import *

MAIN_URL = 'http://aws.amazon.com/ec2/pricing/'
SAMPLE_URLS = [
    '//a0.awsstatic.com/pricing/1/ec2/linux-od.min.js',
    '//a0.awsstatic.com/pricing/1/ec2/rhel-od.min.js',
    ]
SAMPLE_CONTENT = {
    'http://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js': { 'linux': {} },
    'http://a0.awsstatic.com/pricing/1/ec2/rhel-od.min.js': { 'rhel': {} },
    }
DEFAULT_TEXT = "\n".join(["model: '{}'".format(url) for url in SAMPLE_URLS])

@pytest.fixture
def mock_requests_get():
    class MockRequestsGet(object):
        def __call__(self, url):
            self.url = url
            return self
    
        def __init__(self, text=DEFAULT_TEXT):
            self.url = ''
            self.text = text

    return MockRequestsGet()

@pytest.fixture
def mock_process_model():
    class MockProcessModel(object):
        def __call__(self, url, instances):
            self.urls.append(url)
            instances.update(SAMPLE_CONTENT[url])
            return instances

        def __init__(self):
            self.urls = []

    return MockProcessModel()

def test_model_ec2(monkeypatch, mock_requests_get, mock_process_model):
    monkeypatch.setattr('requests.get', mock_requests_get)
    monkeypatch.setattr(
        'accloudtant.prices.aws.process_model',
        mock_process_model
        )
    result = process_ec2()
    assert(mock_requests_get.url == MAIN_URL)
    for url in SAMPLE_URLS:
        assert('http:{}'.format(url) in mock_process_model.urls)
    assert(result == {'linux': {}, 'rhel': {}})
