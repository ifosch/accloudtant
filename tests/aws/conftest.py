import warnings
import pytest
import accloudtant.aws.prices


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


@pytest.fixture(scope="session")
def ec2_resource():
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


@pytest.fixture(scope="session")
def ec2_client():
    class MockEC2Client(object):
        def __init__(self, instances, reserved):
            self.instances = instances
            self.reserved = reserved

        def describe_instances(self):
            return self.instances

        def describe_reserved_instances(self):
            return self.reserved

    class MockEC2ClientCall(object):
        def set_responses(self, instances=None, reserved=None):
            if instances is None:
                instances = {}
            if reserved is None:
                reserved = {}
            self.instances = instances
            self.reserved = reserved

        def __call__(self, *args):
            return MockEC2Client(self.instances, self.reserved)

    return MockEC2ClientCall()


@pytest.fixture
def mock_requests_get():
    class MockRequestsGet(object):
        def set_responses(self, responses=None):
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

        def __init__(self, responses=None):
            self.set_responses(responses)
            self.urls = []
            self.text = 'Default response'

    return MockRequestsGet()


@pytest.fixture
def process_ec2():
    class MockProcessEC2(object):
        def set_responses(self, responses=None, unknown=None):
            if responses is None:
                responses = {}
            if unknown is None:
                unknown = []
            self.responses = responses
            self.unknown = unknown

        def __call__(self, url):
            for name in self.unknown:
                warnings.warn("WARN: Parser not implemented for {}"
                              .format(name))
            return self.responses

        def __init__(self, responses=None):
            self.set_responses(responses)

    return MockProcessEC2()


@pytest.fixture
def mock_process_model():
    class MockProcessModel(object):
        def set_responses(self, responses=None):
            if responses is None:
                responses = {}
            self.responses = responses

        def __call__(self, url, instances):
            self.urls.append(url)
            instances.update(self.responses[url])
            return instances

        def __init__(self, responses=None):
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


@pytest.fixture
def mock_process_generic():
    class MockProcessGeneric(object):
        def __call__(self, data, js_name, instances):
            section = accloudtant.aws.prices.section_names[js_name]
            generic = {
                'version': "0.1",
                'kind': section['kind'],
                'key': section['key'],
                }
            instances = instances or {}
            processed_data = {}
            instances.update({section['kind']: processed_data, })
            return generic, instances

    return MockProcessGeneric()
