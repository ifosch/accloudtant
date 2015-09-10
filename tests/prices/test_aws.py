import pytest
from accloudtant.prices.aws import *

@pytest.fixture
def mock_requests_get():
    class MockRequestsGet(object):
        def set_responses(self, responses = None):
            if responses is None:
                responses = {}
            self.responses = responses

        def __call__(self, url):
            self.urls.append(url)
            if url in self.responses:
                self.text = self.responses[url]
            else:
                self.text = 'Default response'
            return self
    
        def __init__(self, responses = None):
            self.set_responses(responses)
            self.urls = []
            self.text = 'Default response'

    return MockRequestsGet()

@pytest.fixture
def mock_process_model():
    class MockProcessModel(object):
        def set_responses(self, responses = None):
            if responses is None:
                responses = {}
            self.responses = responses

        def __call__(self, url, instances):
            self.urls.append(url)
            instances.update(self.responses[url])
            return instances

        def __init__(self, responses = None):
            self.urls = []
            self.set_responses(responses)

    return MockProcessModel()

@pytest.fixture
def mock_processor():
    class MockProcessor(object):
        def __call__(self, data, js_name, instances):
            self.data_sets.append(data)
            instances.update(data)
            return instances

        def __init__(self):
            self.data_sets = []

    return MockProcessor()

def test_model_ec2(monkeypatch, mock_requests_get, mock_process_model):
    sample_content = {
        'http://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js': { 'linux': {} },
        'http://a0.awsstatic.com/pricing/1/ec2/rhel-od.min.js': { 'rhel': {} },
        }
    sample_urls = [
        '//a0.awsstatic.com/pricing/1/ec2/linux-od.min.js',
        '//a0.awsstatic.com/pricing/1/ec2/rhel-od.min.js',
        ]
    main_reply = "\n".join(["model: '{}'".format(url) for url in sample_urls])
    main_url = 'http://aws.amazon.com/ec2/pricing/'

    monkeypatch.setattr('requests.get', mock_requests_get)
    mock_requests_get.set_responses({ main_url: main_reply })
    monkeypatch.setattr(
        'accloudtant.prices.aws.process_model',
        mock_process_model
        )
    mock_process_model.set_responses(sample_content)

    result = process_ec2()

    assert(main_url in mock_requests_get.urls)
    for url in sample_urls:
        assert('http:{}'.format(url) in mock_process_model.urls)
    assert(result == {'linux': {}, 'rhel': {}})

def test_model_process(monkeypatch, mock_requests_get, mock_processor):
    sample_urls = {
        'http://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js',
        'http://a0.awsstatic.com/pricing/1/ec2/rhel-od.min.js',
        }
    sample_content = {
        'http://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js': 'callback({xxx: "xxx"})',
        'http://a0.awsstatic.com/pricing/1/ec2/rhel-od.min.js': 'callback({yyy: "yyy"})',
        }

    monkeypatch.setattr('requests.get', mock_requests_get)
    mock_requests_get.set_responses(sample_content)
    monkeypatch.setattr('accloudtant.prices.aws.section_names', {
        'linux-od.min.js': {
           'process': mock_processor,
           },
        'rhel-od.min.js': {
           'process': mock_processor,
           },
        })

    result = None
    for url in sample_urls:
        result = process_model(url, result)

    for url in sample_content:
        assert(url in mock_requests_get.urls)
    assert(result == {'xxx': 'xxx', 'yyy': 'yyy'})
