#!/usr/bin/env python
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

from os import environ
import io
import json
import re
import warnings
import requests
from tabulate import tabulate
from accloudtant.utils import fix_lazy_json


class Prices(object):
    def __init__(self):
        with warnings.catch_warnings(record=True) as price_warnings:
            curr_url = 'http://aws.amazon.com/ec2/pricing/'
            prev_url = 'http://aws.amazon.com/ec2/previous-generation/'
            self.prices = process_ec2(curr_url)
            prices_prev = process_ec2(prev_url)
            for kind in self.prices:
                if kind in prices_prev:
                    self.update_region_prices(prices_prev, kind)
            self.output = print_prices(self.prices)
            for warning in price_warnings:
                self.output += "\n{}".format(warning.message)

    def update_region_prices(self, prices_prev, kind):
        for region in self.prices[kind]:
            region_prices = self.prices[kind][region]
            if region in prices_prev[kind]:
                region_prices.update(prices_prev[kind][region])

    def __repr__(self):
        return self.output


def eval_price_exists(price):
    return price or 'N/A'


def print_prices(instances=None, region='us-east-1'):
    """ This function prints the results from the AWS EC2 pricing
        processing."""
    if 'AWS_DEFAULT_REGION' in environ:
        region = environ['AWS_DEFAULT_REGION']
    empty_ri = {
        'yrTerm1': {
            'noUpfront': {
                'effectiveHourly': None,
            },
            'partialUpfront': {
                'effectiveHourly': None,
            },
            'allUpfront': {
                'effectiveHourly': None,
            },
        },
        'yrTerm3': {
            'noUpfront': {
                'effectiveHourly': None,
            },
            'partialUpfront': {
                'effectiveHourly': None,
            },
            'allUpfront': {
                'effectiveHourly': None,
            },
        },
    }
    headers = ['Type',
               'On Demand',
               '1y No Upfront',
               '1y Partial Upfront',
               '1y All Upfront',
               '3y Partial Upfront',
               '3y All Upfront']
    table = []
    for ec2_kind in ['linux']:
        for size in sorted(instances[ec2_kind][region].keys()):
            instance_size = instances[ec2_kind][region][size]
            on_demand = instance_size['od']
            reserved_prices = instance_size.get('ri', empty_ri)
            rsrvd_1yr = reserved_prices['yrTerm1']
            rsrvd_3yr = reserved_prices['yrTerm3']
            no_upfront = 'noUpfront'
            partial_upfront = 'partialUpfront'
            all_upfront = 'allUpfront'
            hourly_price = rsrvd_1yr[no_upfront]['effectiveHourly']
            no_upfront = eval_price_exists(hourly_price)
            hourly_price = rsrvd_1yr[partial_upfront]['effectiveHourly']
            partial_upfront_1yr = eval_price_exists(hourly_price)
            hourly_price = rsrvd_1yr[all_upfront]['effectiveHourly']
            all_upfront_1yr = eval_price_exists(hourly_price)
            hourly_price = rsrvd_3yr[partial_upfront]['effectiveHourly']
            partial_upfront_3yr = eval_price_exists(hourly_price)
            hourly_price = rsrvd_3yr[all_upfront]['effectiveHourly']
            all_upfront_3yr = eval_price_exists(hourly_price)
            row = [size,
                   on_demand,
                   no_upfront,
                   partial_upfront_1yr,
                   all_upfront_1yr,
                   partial_upfront_3yr,
                   all_upfront_3yr]
            table.append(row)
    output = "EC2 (Hourly prices, no upfronts, no instance type features):\n"
    output += tabulate(table, headers)
    return output


def process_ec2(url):
    """
    This function drives the AWS EC2 pricing processing.
    """
    instances = {}
    pricings = requests.get(url)
    for html_line in io.StringIO(pricings.text):
        if 'model:' in html_line:
            url = re.sub(r".+'(.+)'.*", r"http:\1", html_line.strip())
            instances = process_model(url, instances)
    return instances


def process_model(url, instances=None):
    """
    Given the URL of a AWS JS pricing table generator, invokes the
    corresponding processing function according to SECTION_NAMES.
    """
    if instances is None:
        instances = {}
    js_name = url.split('/')[-1]
    pricing = requests.get(url)
    for js_line in io.StringIO(pricing.text.replace("\n", "")):
        if 'callback' in js_line:
            data = fix_lazy_json(re.sub(r".*callback\((.+)\).*",
                                        r"\1", js_line))
            data = json.loads(data)
    if js_name not in SECTION_NAMES:
        processor = process_not_implemented
    else:
        processor = SECTION_NAMES[js_name]['process']
    instances = processor(data, js_name, instances)
    return instances


def process_generic(data, js_name, instances=None):
    """
    Given a JSON with AWS pricing for a section, returns generic parameters.
    """
    if js_name in SECTION_NAMES:
        key = SECTION_NAMES[js_name]['key']
        kind = SECTION_NAMES[js_name]['kind']
        name = SECTION_NAMES[js_name]['name']
    else:
        key = None
        kind = None
        name = 'Unknown'
    generic = {
        'version': data['vers'],
        'rate': data['config'].get('rate'),
        'currencies': data['config']['currencies'],
        'regions': len(data['config']['regions']),
        'key': key,
        'kind': kind,
        'name': name,
    }
    instances = instances or {generic['kind']: {}, }
    if generic['kind'] not in instances:
        instances[generic['kind']] = {}
    return generic, instances


def process_od_types(types, instances_region, key):
    for instance_type in types:
        for size in instance_type.get('sizes', []):
            size_name = size['size']
            if size_name not in instances_region:
                instances_region[size_name] = {}
            instance_data = instances_region[size_name]
            instance_data['vCPU'] = size.get('vCPU')
            instance_data['memoryGiB'] = size.get('memoryGiB')
            instance_data['storageGB'] = size.get('storageGB')
            price = size['valueColumns'][0]['prices']['USD']
            instance_data[key] = price


def init_region(instances_kind, region):
    if region not in instances_kind:
        instances_kind[region] = {}


def process_on_demand(data, js_name, instances=None):
    """
    Given the JSON for the On Demand EC2 Instances AWS pricing, it loads
    instance attributes and On Demand pricing into instances dict.
    """
    generic, instances = process_generic(data, js_name, instances)
    for region_data in data['config']['regions']:
        region = region_data['region']
        init_region(instances[generic['kind']], region)
        types = region_data['instanceTypes']
        instances_region = instances[generic['kind']][region]
        process_od_types(types, instances_region, generic['key'])
    return instances


def process_purchase_options(purchase_options, reserved_instances, term_name):
    for purchase_option in purchase_options:
        po_name = purchase_option['purchaseOption']
        prices = {}
        for value in purchase_option['valueColumns']:
            prices[value['name']] = value['prices']['USD']
        reserved_instances[term_name][po_name] = prices


def process_terms(terms, instances):
    for term in terms:
        name = term['term']
        purchase_options = term['purchaseOptions']
        if 'ri' not in instances:
            instances['ri'] = {}
        if name not in instances['ri']:
            instances['ri'][name] = {}
            ris = instances['ri']
            process_purchase_options(purchase_options, ris, name)


def process_types(types, instances, key):
    for instance_type in types:
        size_name = instance_type['type']
        if size_name not in instances:
            instances[size_name] = {}
        instance_data = instances[size_name]
        instance_data[key] = {}
        process_terms(instance_type['terms'], instance_data)


def process_reserved(data, js_name, instances=None):
    """
    Given the JSON for the Reserved EC2 Instances AWS pricing, it loads
    Reserved pricing into instances dict.
    """
    generic, instances = process_generic(data, js_name, instances)
    for region_data in data['config']['regions']:
        region = region_data['region']
        init_region(instances[generic['kind']], region)
        types = region_data['instanceTypes']
        region_instances = instances[generic['kind']][region]
        key = generic['key']
        process_types(types, region_instances, key)
    return instances


def process_data_xfer_types(types, section):
    for dt_type in types:
        type_name = dt_type['name']
        if type_name not in section:
            section[type_name] = {}
        for dt_tier in dt_type['tiers']:
            price = dt_tier['prices']['USD']
            if len(price):
                section[type_name][dt_tier['name']] = price


def process_data_transfer(data, js_name, instances=None):
    """
    Given the JSON for the Data Transfer pricing, it loads Data Transfer
    pricing into instances dict.
    """
    generic, instances = process_generic(data, js_name, instances)
    for region_data in data['config']['regions']:
        region = region_data['region']
        init_region(instances[generic['kind']], region)
        section = instances[generic['kind']][region]
        section['regional'] = region_data['regionalDataTransfer']
        section['ELB'] = region_data['elasticLBDataTransfer']
        section['AZ'] = region_data['azDataTransfer']
        process_data_xfer_types(region_data['types'], section)
    return instances


def set_price(instance_data, name, price):
    instance_data[name] = price


def process_ebs_cw(data, js_name, instances=None):
    """
    Given the JSON for the EBS pricing, it loads EBS pricing into instances
    dict.
    """
    generic, instances = process_generic(data, js_name, instances)
    for region_data in data['config']['regions']:
        region = region_data['region']
        if region not in instances[generic['kind']]:
            instances[generic['kind']][region] = {}
        for price_type in region_data['types']:
            price = price_type['values'][0]['prices']['USD']
            instance_data = instances[generic['kind']][region]
            set_price(instance_data, price_type['name'], price)
    return instances


def process_eip_elb(data, js_name, instances=None):
    """
    Given the JSON for the EIP pricing, it loads EIP pricing into instances
    dict.
    """
    generic, instances = process_generic(data, js_name, instances)
    for region_data in data['config']['regions']:
        region = region_data['region']
        init_region(instances[generic['kind']], region)
        for price_type in region_data['types'][0]['values']:
            price = price_type['prices']['USD']
            instance_data = instances[generic['kind']][region]
            set_price(instance_data, price_type['rate'], price)
    return instances


def process_not_implemented(data, js_name, instances=None):
    """
    Given the JSON of a AWS pricing section which was not-implemented.
    """
    generic, instances = process_generic(data, js_name, instances)
    warnings.warn("WARN: Parser not implemented for {}".format(
        generic['name']))
    return instances

SECTION_NAMES = {
    'linux-od.min.js': {
        'name': 'On Demand - Linux',
        'key': 'od',
        'kind': 'linux',
        'process': process_on_demand,
    },
    'rhel-od.min.js': {
        'name': 'On Demand - RHEL',
        'key': 'od',
        'kind': 'rhel',
        'process': process_on_demand,
    },
    'sles-od.min.js': {
        'name': 'On Demand - SLES',
        'key': 'od',
        'kind': 'suse',
        'process': process_on_demand,
    },
    'mswin-od.min.js': {
        'name': 'On Demand - Windows',
        'key': 'od',
        'kind': 'win',
        'process': process_on_demand,
    },
    'mswinSQL-od.min.js': {
        'name': 'On Demand - Windows with SQL Server Standard',
        'key': 'od',
        'kind': 'winsql',
        'process': process_on_demand,
    },
    'mswinSQLWeb-od.min.js': {
        'name': 'On Demand - Windows with SQL Server Web',
        'key': 'od',
        'kind': 'winsqlweb',
        'process': process_on_demand,
    },
    'mswinSQLEnterprise-od.min.js': {
        'name': 'On Demand - Windows with SQL Server Enterprise',
        'key': 'od',
        'kind': 'winsqlent',
        'process': process_on_demand,
    },
    'linux-unix-shared.min.js': {
        'name': 'Reserved - Linux',
        'key': 'ri',
        'kind': 'linux',
        'process': process_reserved,
    },
    'red-hat-enterprise-linux-shared.min.js': {
        'name': 'Reserved - RHEL',
        'key': 'ri',
        'kind': 'rhel',
        'process': process_reserved,
    },
    'suse-linux-shared.min.js': {
        'name': 'Reserved - SLES',
        'key': 'ri',
        'kind': 'suse',
        'process': process_reserved,
    },
    'windows-shared.min.js': {
        'name': 'Reserved - Linux',
        'key': 'ri',
        'kind': 'win',
        'process': process_reserved,
    },
    'windows-with-sql-server-standard-shared.min.js': {
        'name': 'Reserved - Windows with SQL Server Standard',
        'key': 'ri',
        'kind': 'winsql',
        'process': process_reserved,
    },
    'windows-with-sql-server-web-shared.min.js': {
        'name': 'Reserved - Windows with SQL Server Web',
        'key': 'ri',
        'kind': 'winsqlweb',
        'process': process_reserved,
    },
    'windows-with-sql-server-enterprise-shared.min.js': {
        'name': 'Reserved - Windows with SQL Server Enterprise',
        'key': 'ri',
        'kind': 'winsqlent',
        'process': process_reserved,
    },
    'spot.js': {
        'name': 'Spot Instances',
        'key': 'si',
        'kind': 'other',
        'process': process_not_implemented,
    },
    'pricing-data-transfer-with-regions.min.js': {
        'name': 'Data Transfer',
        'key': 'dt',
        'kind': 'data_transfer',
        'process': process_data_transfer,
    },
    'pricing-ebs-optimized-instances.min.js': {
        'name': 'EBS-Optimized Instances',
        'key': 'oi',
        'kind': 'other',
        'process': process_not_implemented,
    },
    'pricing-ebs.min.js': {
        'name': 'Amazon Elastic Block Store',
        'key': 'bs',
        'kind': 'ebs',
        'process': process_ebs_cw,
    },
    'pricing-elastic-ips.min.js': {
        'name': 'Elastic IP Addresses',
        'key': 'ei',
        'kind': 'eip',
        'process': process_eip_elb,
    },
    'pricing-cloudwatch.min.js': {
        'name': 'Amazon CloudWatch',
        'key': 'cw',
        'kind': 'cw',
        'process': process_ebs_cw,
    },
    'pricing-elb.min.js': {
        'name': 'Elastic Load Balancing',
        'key': 'lb',
        'kind': 'elb',
        'process': process_eip_elb,
    },
}
