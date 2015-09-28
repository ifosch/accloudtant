import pytest
import accloudtant.aws.prices


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
def mock_process_ec2():
    class MockProcessEC2(object):
        def set_responses(self, responses=None):
            if responses is None:
                responses = {}
            self.responses = responses

        def __call__(self):
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


def test_model_ec2(monkeypatch, mock_requests_get, mock_process_model):
    sample_content = {
        'http://a0.aws.com/pricing/1/ec2/linux-od.min.js': {'linux': {}, },
        'http://a0.aws.com/pricing/1/ec2/rhel-od.min.js': {'rhel': {}, },
        }
    sample_urls = [
        '//a0.aws.com/pricing/1/ec2/linux-od.min.js',
        '//a0.aws.com/pricing/1/ec2/rhel-od.min.js',
        ]
    main_reply = "\n".join(["model: '{}'".format(url) for url in sample_urls])
    main_url = 'http://aws.amazon.com/ec2/pricing/'

    monkeypatch.setattr('requests.get', mock_requests_get)
    mock_requests_get.set_responses({main_url: main_reply, })
    monkeypatch.setattr(
        'accloudtant.aws.prices.process_model',
        mock_process_model
        )
    mock_process_model.set_responses(sample_content)

    result = accloudtant.aws.prices.process_ec2()

    assert(main_url in mock_requests_get.urls)
    for url in sample_urls:
        assert('http:{}'.format(url) in mock_process_model.urls)
    assert(result == {'linux': {}, 'rhel': {}})


def test_process_model(monkeypatch, mock_requests_get, mock_processor):
    sample_urls = {
        'http://ec2/linux-od.min.js',
        'http://ec2/rhel-od.min.js',
        }
    sample_content = {
        'http://ec2/linux-od.min.js': 'callback({xxx: "xxx"})',
        'http://ec2/rhel-od.min.js': 'callback({yyy: "yyy"})',
        }

    monkeypatch.setattr('requests.get', mock_requests_get)
    mock_requests_get.set_responses(sample_content)
    monkeypatch.setattr('accloudtant.aws.prices.section_names', {
        'linux-od.min.js': {
           'process': mock_processor,
           },
        'rhel-od.min.js': {
           'process': mock_processor,
           },
        })

    result = None
    for url in sample_urls:
        result = accloudtant.aws.prices.process_model(url, result)

    for url in sample_content:
        assert(url in mock_requests_get.urls)
    assert(result == {'xxx': 'xxx', 'yyy': 'yyy'})


def test_process_generic(monkeypatch):
    data_no_rate = {
        'vers': "0.1",
        'config': {
            'currencies': ['USD'],
            'regions': [],
            },
        }
    data_rate = {
        'vers': "0.1",
        'config': {
            'rate': 'perh',
            'currencies': ['USD'],
            'regions': [],
            },
        }
    sample_content = {
        'http://ec2/linux-od.min.js': data_no_rate,
        'http://ec2/rhel-od.min.js': data_rate,
        }

    monkeypatch.setattr('accloudtant.aws.prices.section_names', {
        'linux-od.min.js': {
            'key': 'od',
            'kind': 'linux',
            'name': 'On Demand - Linux',
           },
        'rhel-od.min.js': {
            'key': 'od',
            'kind': 'rhel',
            'name': 'On Demand - RHEL',
           },
        })

    instances = None
    for url, data in sample_content.items():
        js_name = url.split('/')[-1]
        generic, instances = accloudtant.aws.prices.process_generic(
                data, js_name, instances)
        assert(generic['version'] == data['vers'])
        if 'rate' in data['config']:
            assert(generic['rate'] == data['config']['rate'])
    assert('linux' in instances and 'rhel' in instances)


def test_process_on_demand(monkeypatch, mock_process_generic):
    data_rate = {
        'vers': "0.1",
        'config': {
            'rate': 'perh',
            'currencies': ['USD'],
            'regions': [{
                    'region': 'us-east-1',
                    'instanceTypes': [{
                        'type': 'generalCurrentGen',
                        'sizes': [{
                                'size': 't2.micro',
                                'vCPU': '1',
                                'memoryGiB': '1',
                                'storageGB': 'ebsonly',
                                'valueColumns': [{
                                    'prices': {'USD': '0.01', },
                                    }, ],
                                }, ],
                            }, ],
                    }, {
                    'region': 'us-west-1',
                    'instanceTypes': [{
                        'type': 'generalCurrentGen',
                        'sizes': [{
                            'size': 't2.micro',
                            'vCPU': '1',
                            'memoryGiB': '1',
                            'storageGB': 'ebsonly',
                            'valueColumns': [{
                                'prices': {'USD': '0.01', },
                                }, ],
                            }, ],
                        }, ],
                    }, ],
            },
        }
    sample_content = {
        'http://ec2/linux-od.min.js': data_rate,
        'http://ec2/rhel-od.min.js': data_rate,
        }

    monkeypatch.setattr(
        'accloudtant.aws.prices.process_generic',
        mock_process_generic
        )

    instances = None
    for url, data in sample_content.items():
        js_name = url.split('/')[-1]
        instances = accloudtant.aws.prices.process_on_demand(
                data, js_name, instances)
    regions = [region['region'] for region in data_rate['config']['regions']]
    assert('linux' in instances and 'rhel' in instances)
    for kind in instances:
        assert(region in instances[kind] for region in regions)
        for region in instances[kind]:
            assert('t2.micro' in instances[kind][region])
            instance_size = instances[kind][region]['t2.micro']
            assert(instance_size['vCPU'] == '1')
            assert(instance_size['memoryGiB'] == '1')
            assert(instance_size['storageGB'] == 'ebsonly')
            assert(instance_size['od'] == '0.01')


def test_process_reserved(monkeypatch, mock_process_generic):
    data_rate = {
        'vers': "0.1",
        'config': {
            'rate': 'perh',
            'currencies': ['USD'],
            'regions': [{
                'region': 'us-east-1',
                'instanceTypes': [{
                  'type': 't2.micro',
                  'terms': [{
                      'term': 'yrTerm1',
                      'purchaseOptions': [{
                          'purchaseOption': 'noUpfront',
                          'savingsOverOD': '31%',
                          'valueColumns': [{
                              'name': 'upfront',
                              'prices': {'USD': '0', },
                              }, {
                              'name': 'monthlyStar',
                              'prices': {'USD': '6.57', },
                              }, {
                              'name': 'effectiveHourly',
                              'prices': {'USD': '0.009', },
                              }, ],
                          }, {
                          'purchaseOption': 'partialUpfront',
                          'savingsOverOD': '32%',
                          'valueColumns': [{
                              'name': 'upfront',
                              'prices': {'USD': '51', },
                              }, {
                              'name': 'monthlyStar',
                              'prices': {'USD': '2.19', },
                              }, {
                              'name': 'effectiveHourly',
                              'prices': {'USD': '0.0088', },
                              }, ],
                          }, {
                          'purchaseOption': 'allUpfront',
                          'savingsOverOD': '34%',
                          'valueColumns': [{
                              'name': 'upfront',
                              'prices': {'USD': '75', },
                              }, {
                              'name': 'monthlyStar',
                              'prices': {'USD': '0', },
                              }, {
                              'name': 'effectiveHourly',
                              'prices': {'USD': '0.0086', },
                              }, ],
                          }, ]
                      }, {
                      'term': 'yrTerm3',
                      'purchaseOptions': [{
                          'purchaseOption': 'partialUpfront',
                          'savingsOverOD': '53%',
                          'valueColumns': [{
                              'name': 'upfront',
                              'prices': {'USD': '109', },
                              }, {
                              'name': 'monthlyStar',
                              'prices': {'USD': '1.46', },
                              }, {
                              'name': 'effectiveHourly',
                              'prices': {'USD': '0.0061', },
                              }, ],
                          }, {
                          'purchaseOption': 'allUpfront',
                          'savingsOverOD': '56%',
                          'valueColumns': [{
                              'name': 'upfront',
                              'prices': {'USD': '151', },
                              }, {
                              'name': 'monthlyStar',
                              'prices': {'USD': '0', },
                              }, {
                              'name': 'effectiveHourly',
                              'prices': {'USD': '0.0057', },
                              }, ],
                          }, ]
                      }, ]
                   }, ],
                }, {
                'region': 'us-west-1',
                'instanceTypes': [{
                  'type': 't2.micro',
                  'terms': [{
                      'term': 'yrTerm1',
                      'purchaseOptions': [{
                          'purchaseOption': 'noUpfront',
                          'savingsOverOD': '31%',
                          'valueColumns': [{
                              'name': 'upfront',
                              'prices': {'USD': '0', },
                              }, {
                              'name': 'monthlyStar',
                              'prices': {'USD': '6.57', },
                              }, {
                              'name': 'effectiveHourly',
                              'prices': {'USD': '0.009', },
                              }, ],
                          }, {
                          'purchaseOption': 'partialUpfront',
                          'savingsOverOD': '32%',
                          'valueColumns': [{
                              'name': 'upfront',
                              'prices': {'USD': '51', },
                              }, {
                              'name': 'monthlyStar',
                              'prices': {'USD': '2.19', },
                              }, {
                              'name': 'effectiveHourly',
                              'prices': {'USD': '0.0088', },
                              }, ],
                          }, {
                          'purchaseOption': 'allUpfront',
                          'savingsOverOD': '34%',
                          'valueColumns': [{
                              'name': 'upfront',
                              'prices': {'USD': '75', },
                              }, {
                              'name': 'monthlyStar',
                              'prices': {'USD': '0', },
                              }, {
                              'name': 'effectiveHourly',
                              'prices': {'USD': '0.0086', },
                              }, ],
                          }, ]
                      }, {
                      'term': 'yrTerm3',
                      'purchaseOptions': [{
                          'purchaseOption': 'partialUpfront',
                          'savingsOverOD': '53%',
                          'valueColumns': [{
                              'name': 'upfront',
                              'prices': {'USD': '109', },
                              }, {
                              'name': 'monthlyStar',
                              'prices': {'USD': '1.46', },
                              }, {
                              'name': 'effectiveHourly',
                              'prices': {'USD': '0.0061', },
                              }, ],
                          }, {
                          'purchaseOption': 'allUpfront',
                          'savingsOverOD': '56%',
                          'valueColumns': [{
                              'name': 'upfront',
                              'prices': {'USD': '151', },
                              }, {
                              'name': 'monthlyStar',
                              'prices': {'USD': '0', },
                              }, {
                              'name': 'effectiveHourly',
                              'prices': {'USD': '0.0057', },
                              }, ],
                          }, ],
                      }, ],
                  }, ],
                }, ],
            },
        }
    sample_content = {
        'http://ec2/linux-unix-shared.min.js': data_rate,
        'http://ec2/red-hat-enterprise-linux-shared.min.js': data_rate,
        }

    monkeypatch.setattr(
        'accloudtant.aws.prices.process_generic',
        mock_process_generic
        )

    instances = None
    for url, data in sample_content.items():
        js_name = url.split('/')[-1]
        instances = accloudtant.aws.prices.process_reserved(
                data, js_name, instances)
    assert('linux' in instances and 'rhel' in instances)
    regions = [region['region'] for region in data_rate['config']['regions']]
    for kind in instances:
        assert(region in instances[kind] for region in regions)
        for region in instances[kind]:
            assert('t2.micro' in instances[kind][region])
            instance_size = instances[kind][region]['t2.micro']
            assert('ri' in instance_size)
            instance_reserved = instance_size['ri']
            terms = ['yrTerm1', 'yrTerm3']
            assert(term in instance_reserved for term in terms)
            for term in terms:
                for purchase_opt in ['partialUpfront', 'allUpfront']:
                    assert(purchase_opt in instance_reserved[term])
                    purchase_parts = instance_reserved[term][purchase_opt]
                    assert('upfront' in purchase_parts)
                    assert('monthlyStar' in purchase_parts)
                    assert('effectiveHourly' in purchase_parts)
            assert('noUpfront' in instance_reserved['yrTerm1'])
            no_upfront = instance_reserved['yrTerm1']['noUpfront']
            assert(no_upfront['upfront'] == '0')
            assert(no_upfront['monthlyStar'] == '6.57')
            assert(no_upfront['effectiveHourly'] == '0.009')


def test_process_data_transfer(monkeypatch, mock_process_generic):
    data = {
        'vers': "0.1",
        'config': {
            'rate': 'perh',
            'currencies': ['USD'],
            'regions': [{
                'region': 'us-east-1',
                'types': [{
                    'name': 'dataXferInEC2',
                    'tiers': [{
                        'name': 'Internet',
                        'prices': {'USD': '0.00', },
                        }, {
                        'name': 'anotherRegion',
                        'prices': {'USD': '0.00', },
                        }, {
                        'name': 'anotherService',
                        'prices': {'USD': '0.00', },
                        }, {
                        'name': 'sameAZText',
                        'prices': {'USD': '', },
                        }, {
                        'name': 'sameAZprivateIP',
                        'prices': {'USD': '0.00', },
                        }, {
                        'name': 'sameAZpublicIP',
                        'prices': {'USD': '0.01', },
                        }, {
                        'name': 'crossAZ',
                        'prices': {'USD': '0.01', },
                        }, ],
                    }, {
                    'name': 'dataXferOutEC2',
                    'tiers': [{
                        'name': 'anotherServiceOut',
                        'prices': {'USD': '0.00', },
                        }, {
                        'name': 'sameAZTextOut',
                        'prices': {'USD': '', },
                        }, {
                        'name': 'sameAZprivateIPOut',
                        'prices': {'USD': '0.00', },
                        }, {
                        'name': 'sameAZpublicIPOut',
                        'prices': {'USD': '0.01', },
                        }, {
                        'name': 'crossAZOut',
                        'prices': {'USD': '0.01', },
                        }, {
                        'name': 'crossRegion',
                        'prices': {'USD': '0.02', },
                        }, {
                        'name': 'Amazon CloudFront',
                        'prices': {'USD': '0.00', },
                        }, ],
                    }, {
                    'name': 'dataXferOutInternet',
                    'tiers': [{
                        'name': 'firstGBout',
                        'prices': {'USD': '0.00', },
                        }, {
                        'name': 'upTo10TBout',
                        'prices': {'USD': '0.09', },
                        }, {
                        'name': 'next40TBout',
                        'prices': {'USD': '0.085', },
                        }, {
                        'name': 'next100TBout',
                        'prices': {'USD': '0.07', },
                        }, {
                        'name': 'next350TBout',
                        'prices': {'USD': '0.05', },
                        }, {
                        'name': 'next05PBout',
                        'prices': {'USD': 'contactus', },
                        }, {
                        'name': 'next4PBout',
                        'prices': {'USD': 'contactus', },
                        }, {
                        'name': 'greater5PBout',
                        'prices': {'USD': 'contactus', },
                        }, ],
                    }, ],
                'azDataTransfer': {'prices': {'USD': '0.00', }, },
                'regionalDataTransfer': {'prices': {'USD': '0.01', }, },
                'elasticLBDataTransfer': {
                    'prices': {'USD': '0.01', },
                    'rate': 'perGBin/out',
                    },
                }, ],
            },
        }

    monkeypatch.setattr(
        'accloudtant.aws.prices.process_generic',
        mock_process_generic
        )

    instances = None
    js_name = 'pricing-data-transfer-with-regions.min.js'
    instances = accloudtant.aws.prices.process_data_transfer(
            data, js_name, instances)
    assert('data_transfer' in instances)
    regions = [region['region'] for region in data['config']['regions']]
    for region in regions:
        region_data = instances['data_transfer'][region]
        assert('dataXferInEC2' in region_data)
        assert('Internet' in region_data['dataXferInEC2'])
        assert('anotherRegion' in region_data['dataXferInEC2'])
        assert('anotherService' in region_data['dataXferInEC2'])
        assert('sameAZText' not in region_data['dataXferInEC2'])
        assert('sameAZprivateIP' in region_data['dataXferInEC2'])
        assert('sameAZpublicIP' in region_data['dataXferInEC2'])
        assert('crossAZ' in region_data['dataXferInEC2'])
        assert('dataXferOutEC2' in region_data)
        assert('anotherServiceOut' in region_data['dataXferOutEC2'])
        assert('sameAZTextOut' not in region_data['dataXferOutEC2'])
        assert('sameAZprivateIPOut' in region_data['dataXferOutEC2'])
        assert('sameAZpublicIPOut' in region_data['dataXferOutEC2'])
        assert('crossAZOut' in region_data['dataXferOutEC2'])
        assert('crossRegion' in region_data['dataXferOutEC2'])
        assert('Amazon CloudFront' in region_data['dataXferOutEC2'])
        assert('dataXferOutInternet' in region_data)
        assert('firstGBout' in region_data['dataXferOutInternet'])
        assert('upTo10TBout' in region_data['dataXferOutInternet'])
        assert('next40TBout' in region_data['dataXferOutInternet'])
        assert('next100TBout' in region_data['dataXferOutInternet'])
        assert('next350TBout' in region_data['dataXferOutInternet'])
        assert('next05PBout' in region_data['dataXferOutInternet'])
        assert('next4PBout' in region_data['dataXferOutInternet'])
        assert('greater5PBout' in region_data['dataXferOutInternet'])
        assert('AZ' in region_data)
        assert('regional' in region_data)
        assert('ELB' in region_data)


def test_process_ebs(monkeypatch, mock_process_generic):
    data = {
        'vers': "0.1",
        'config': {
            'rate': 'perh',
            'currencies': ['USD'],
            'regions': [{
                'region': 'us-east',
                'types': [{
                    'name': 'ebsVols',
                    'values': [{
                        'prices': {'USD': '0.10', },
                        'rate': 'perGBmoProvStorage',
                        }, {
                        'prices': {'USD': '0.10', },
                        'rate': 'perMMIOreq',
                        }, ],
                    }, {
                    'name': 'ebsPIOPSVols',
                    'values': [{
                        'prices': {'USD': '0.125', },
                        'rate': 'perGBmoProvStorage',
                        }, {
                        'prices': {'USD': '0.10', },
                        'rate': 'perPIOPSreq',
                        }, ],
                    }, {
                    'name': 'ebsSnapsToS3',
                    'values': [{
                        'prices': {'USD': '0.095', },
                        'rate': 'perGBmoDataStored',
                        }, ],
                    }, ],
                }, ],
            },
        }

    monkeypatch.setattr(
        'accloudtant.aws.prices.process_generic',
        mock_process_generic
        )

    instances = None
    js_name = 'pricing-ebs.min.js'
    instances = accloudtant.aws.prices.process_ebs(data, js_name, instances)
    assert('ebs' in instances)
    regions = [region['region'] for region in data['config']['regions']]
    for region in regions:
        region_data = instances['ebs'][region]
        assert('ebsVols' in region_data)
        assert('ebsPIOPSVols' in region_data)
        assert('ebsSnapsToS3' in region_data)


def test_process_eip(monkeypatch, mock_process_generic):
    data = {
        'vers': "0.1",
        'config': {
            'rate': 'perh',
            'currencies': ['USD'],
            'regions': [{
                'region': 'us-east',
                'types': [{
                    'values': [{
                        'prices': {'USD': '0.00', },
                        'rate': 'oneEIP',
                        }, {
                        'prices': {'USD': '0.005', },
                        'rate': 'perAdditionalEIPPerHour',
                        }, {
                        'prices': {'USD': '0.005', },
                        'rate': 'perNonAttachedPerHour',
                        }, {
                        'prices': {'USD': '0.00', },
                        'rate': 'perRemapFirst100',
                        }, {
                        'prices': {'USD': '0.10', },
                        'rate': 'perRemapOver100',
                        }, ],
                    }, ],
                }, ],
            },
        }

    monkeypatch.setattr(
        'accloudtant.aws.prices.process_generic',
        mock_process_generic
        )

    instances = None
    js_name = 'pricing-elastic-ips.min.js'
    instances = accloudtant.aws.prices.process_eip(data, js_name, instances)
    assert('eip' in instances)
    regions = [region['region'] for region in data['config']['regions']]
    for region in regions:
        region_data = instances['eip'][region]
        assert('oneEIP' in region_data)
        assert('perAdditionalEIPPerHour' in region_data)
        assert('perNonAttachedPerHour' in region_data)
        assert('perRemapFirst100' in region_data)
        assert('perRemapOver100' in region_data)


def test_process_cw(monkeypatch, mock_process_generic):
    data = {
        'vers': "0.1",
        'config': {
            'rate': 'perh',
            'currencies': ['USD'],
            'regions': [{
                'region': 'us-east',
                'types': [{
                    'name': 'ec2Monitoring',
                    'values': [{
                        'prices': {'USD': '3.50', },
                        'rate': 'cwMetricPerMonth',
                        }, ],
                    }, {
                    'name': 'ec2BasicMonitoring',
                    'values': [{
                        'prices': {'USD': '0.00', },
                        'rate': 'freeOfCharge',
                        }, ],
                    }, {
                    'name': 'cwCustomMetrics',
                    'values': [{
                        'prices': {'USD': '0.50', },
                        'rate': 'cwMetricsPerMonth',
                        }, ],
                    }, ],
                }, ],
            },
        }

    monkeypatch.setattr(
        'accloudtant.aws.prices.process_generic',
        mock_process_generic
        )

    instances = None
    js_name = 'pricing-cloudwatch.min.js'
    instances = accloudtant.aws.prices.process_cw(data, js_name, instances)
    assert('cw' in instances)
    regions = [region['region'] for region in data['config']['regions']]
    for region in regions:
        region_data = instances['cw'][region]
        assert('ec2Monitoring' in region_data)
        assert('ec2BasicMonitoring' in region_data)
        assert('cwCustomMetrics' in region_data)


def test_process_elb(monkeypatch, mock_process_generic):
    data = {
        'vers': "0.1",
        'config': {
            'rate': 'perh',
            'currencies': ['USD'],
            'regions': [{
                'region': 'us-east',
                'types': [{
                    'values': [{
                        'prices': {'USD': '0.025', },
                        'rate': 'perELBHour',
                        }, {
                        'prices': {'USD': '0.008', },
                        'rate': 'perGBProcessed',
                        }, ],
                    }, ],
                }, ],
            },
        }

    monkeypatch.setattr(
        'accloudtant.aws.prices.process_generic',
        mock_process_generic
        )

    instances = None
    js_name = 'pricing-elb.min.js'
    instances = accloudtant.aws.prices.process_elb(data, js_name, instances)
    assert('elb' in instances)
    regions = [region['region'] for region in data['config']['regions']]
    for region in regions:
        region_data = instances['elb'][region]
        assert('perELBHour' in region_data)
        assert('perGBProcessed' in region_data)


def test_print_prices(capsys, monkeypatch, mock_process_ec2):
    result = {
        'eip': {
            'eu-ireland': {
                'perRemapOver100': '0.10',
                'perRemapFirst100': '0.00',
                'oneEIP': '0.00',
                'perNonAttachedPerHour': '0.005',
                'perAdditionalEIPPerHour': '0.005',
                },
            'us-east': {
                'perRemapOver100': '0.10',
                'perRemapFirst100': '0.00',
                'oneEIP': '0.00',
                'perNonAttachedPerHour': '0.005',
                'perAdditionalEIPPerHour': '0.005',
                },
            },
        'cw': {
            'us-west-1': {
                'ec2Monitoring': '3.50',
                'cwRequests': '0.01',
                'cloudWatchLogs': '0.67',
                'cwMetrics': '0.50',
                'cwAlarms': '0.10',
                },
            'us-gov-west-1': {
                'ec2Monitoring': '4.55',
                'cwRequests': '0.013',
                'cwMetrics': '0.65',
                'cwAlarms': '0.0515',
                },
            },
        'ebs': {
            'eu-ireland': {
                'ebsSnapsToS3': '0.138',
                'Amazon EBS General Purpose (SSD) volumes': '0.095',
                'Amazon EBS Provisioned IOPS (SSD) volumes': '0.055',
                'Amazon EBS Magnetic volumes': '0.11',
                },
            'us-east': {
                'ebsSnapsToS3': '0.125',
                'Amazon EBS General Purpose (SSD) volumes': '0.095',
                'Amazon EBS Provisioned IOPS (SSD) volumes': '0.05',
                'Amazon EBS Magnetic volumes': '0.10',
                },
            },
        'data_transfer': {
            'eu-central-1': {
                'regional': {'prices': {'USD': '0.01', }, },
                'ELB': {'prices': {'USD': '0.01', }, },
                'AZ': {'prices': {'USD': '0.00', }, },
                'dataXferInEC2': {
                    'anotherRegion': '0.00',
                    'sameAZprivateIP': '0.00',
                    'anotherService': '0.00',
                    'Internet': '0.00',
                    'crossAZ': '0.01',
                    'sameAZpublicIP': '0.01',
                    },
                'dataXferOutEC2': {
                    'Amazon CloudFront': '0.00',
                    'crossRegion': '0.02',
                    'crossAZOut': '0.01',
                    'anotherServiceOut': '0.00',
                    'sameAZpublicIPOut': '0.01',
                    'sameAZprivateIPOut': '0.00',
                    },
                'dataXferOutInternet': {
                    'next4PBout': 'contactus',
                    'next40TBout': '0.085',
                    'next100TBout': '0.070',
                    'next350TBout': '0.050',
                    'next05PBout': 'contactus',
                    'greater5PBout': 'contactus',
                    'firstGBout': '0.000',
                    'upTo10TBout': '0.090',
                    },
                },
            'us-east-1': {
                'regional': {'prices': {'USD': '0.01', }, },
                'ELB': {'prices': {'USD': '0.01', }, },
                'AZ': {'prices': {'USD': '0.00', }, },
                'dataXferInEC2': {
                    'anotherRegion': '0.00',
                    'sameAZprivateIP': '0.00',
                    'anotherService': '0.00',
                    'Internet': '0.00',
                    'crossAZ': '0.01',
                    'sameAZpublicIP': '0.01',
                    },
                'dataXferOutEC2': {
                    'Amazon CloudFront': '0.00',
                    'crossRegion': '0.02',
                    'crossAZOut': '0.01',
                    'anotherServiceOut': '0.00',
                    'sameAZpublicIPOut': '0.01',
                    'sameAZprivateIPOut': '0.00',
                    },
                'dataXferOutInternet': {
                    'next4PBout': 'contactus',
                    'next40TBout': '0.085',
                    'next100TBout': '0.070',
                    'next350TBout': '0.050',
                    'next05PBout': 'contactus',
                    'greater5PBout': 'contactus',
                    'firstGBout': '0.000',
                    'upTo10TBout': '0.090',
                    },
                },
            },
        'elb': {
            'eu-ireland': {
                'perELBHour': '0.0008',
                'perGBProcessed': '0.028',
                },
            'us-east': {
                'perELBHour': '0.0008',
                'perGBProcessed': '0.025',
                },
            },
        'linux': {
            'eu-west-1': {
                'g2.2xlarge': {
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
                'c3.8xlarge': {
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
            'ap-southeast-1': {
                'g2.2xlarge': {
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
                'c3.8xlarge': {
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

    monkeypatch.setattr(
        'accloudtant.aws.prices.process_ec2',
        mock_process_ec2
        )
    mock_process_ec2.set_responses(result)

    output = """EC2:
"""

    accloudtant.aws.prices.print_prices()
    out, err = capsys.readouterr()
    assert(out == output)
