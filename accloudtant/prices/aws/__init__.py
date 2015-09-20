#!/usr/bin/env python

import io
import json
import re
import warnings
import requests
from accloudtant.utils import fix_lazy_json


def process_ec2():
    """
    This function drives the AWS EC2 pricing processing.
    """
    instances = {}
    pricings = requests.get('http://aws.amazon.com/ec2/pricing/')
    for html_line in io.StringIO(pricings.text):
        if 'model:' in html_line:
            url = re.sub(r".+'(.+)'.*", r"http:\1", html_line.strip())
            instances = process_model(url, instances)
    return instances


def process_model(url, instances=None):
    """
    Given the URL of a AWS JS pricing table generator, invokes the
    corresponding processing function according to section_names.
    """
    if instances is None:
        instances = {}
    js_name = url.split('/')[-1]
    pricing = requests.get(url)
    for js_line in io.StringIO(pricing.text.replace("\n", "")):
        if 'callback' in js_line:
            data = fix_lazy_json(
                    re.sub(r".*callback\((.+)\).*", r"\1", js_line))
            data = json.loads(data)
    processor = section_names[js_name]['process']
    instances = processor(data, js_name, instances)
    return instances


def process_generic(data, js_name, instances=None):
    """
    Given a JSON with AWS pricing for a section, returns generic parameters.
    """
    generic = {
        'version': data['vers'],
        'rate': data['config'].get('rate'),
        'currencies': data['config']['currencies'],
        'regions': len(data['config']['regions']),
        'key': section_names[js_name]['key'],
        'kind': section_names[js_name]['kind'],
        'name': section_names[js_name]['name'],
    }
    instances = instances or {generic['kind']: {}, }
    if generic['kind'] not in instances:
        instances[generic['kind']] = {}
    return generic, instances


def process_on_demand(data, js_name, instances=None):
    """
    Given the JSON for the On Demand EC2 Instances AWS pricing, it loads
    instance attributes and On Demand pricing into instances dict.
    """
    generic, instances = process_generic(data, js_name, instances)
    for region_data in data['config']['regions']:
        region = region_data['region']
        if region not in instances[generic['kind']]:
            instances[generic['kind']][region] = {}
        for instance_type in region_data['instanceTypes']:
            for size in instance_type.get('sizes', []):
                size_name = size['size']
                if size_name not in instances[generic['kind']][region]:
                    instances[generic['kind']][region][size_name] = {}
                instance_data = instances[generic['kind']][region][size_name]
                instance_data['vCPU'] = size.get('vCPU')
                instance_data['memoryGiB'] = size.get('memoryGiB')
                instance_data['storageGB'] = size.get('storageGB')
                price = size['valueColumns'][0]['prices']['USD']
                instance_data[generic['key']] = price
    return instances


def process_reserved(data, js_name, instances=None):
    """
    Given the JSON for the Reserved EC2 Instances AWS pricing, it loads
    Reserved pricing into instances dict.
    """
    generic, instances = process_generic(data, js_name, instances)
    for region_data in data['config']['regions']:
        region = region_data['region']
        if region not in instances[generic['kind']]:
            instances[generic['kind']][region] = {}
        for instance_type in region_data['instanceTypes']:
            size_name = instance_type['type']
            if size_name not in instances[generic['kind']][region]:
                instances[generic['kind']][region][size_name] = {}
            instance_data = instances[generic['kind']][region][size_name]
            instance_data[generic['key']] = {}
            for term in instance_type['terms']:
                term_name = term['term']
                if 'ri' not in instance_data:
                    instance_data['ri'] = {}
                if term_name not in instance_data['ri']:
                    instance_data['ri'][term_name] = {}
                for purchase_option in term['purchaseOptions']:
                    po_name = purchase_option['purchaseOption']
                    prices = {}
                    for value in purchase_option['valueColumns']:
                        prices[value['name']] = value['prices']['USD']
                    instance_data['ri'][term_name][po_name] = prices
    return instances


def process_data_transfer(data, js_name, instances=None):
    """
    Given the JSON for the Data Transfer pricing, it loads Data Transfer
    pricing into instances dict.
    """
    generic, instances = process_generic(data, js_name, instances)
    for region_data in data['config']['regions']:
        region = region_data['region']
        if region not in instances[generic['kind']]:
            instances[generic['kind']][region] = {}
        section = instances[generic['kind']][region]
        section['regional'] = region_data['regionalDataTransfer']
        section['ELB'] = region_data['elasticLBDataTransfer']
        section['AZ'] = region_data['azDataTransfer']
        for dt_type in region_data['types']:
            type_name = dt_type['name']
            if type_name not in section:
                section[type_name] = {}
            for dt_tier in dt_type['tiers']:
                price = dt_tier['prices']['USD']
                if len(price):
                    section[type_name][dt_tier['name']] = price
    return instances


def process_ebs(data, js_name, instances=None):
    """
    Given the JSON for the EBS pricing, it loads EBS pricing into instances
    dict.
    """
    generic, instances = process_generic(data, js_name, instances)
    for region_data in data['config']['regions']:
        region = region_data['region']
        if region not in instances[generic['kind']]:
            instances[generic['kind']][region] = {}
        for ebs_type in region_data['types']:
            price = ebs_type['values'][0]['prices']['USD']
            instances[generic['kind']][region][ebs_type['name']] = price
    return instances


def process_eip(data, js_name, instances=None):
    """
    Given the JSON for the EIP pricing, it loads EIP pricing into instances
    dict.
    """
    generic, instances = process_generic(data, js_name, instances)
    for region_data in data['config']['regions']:
        region = region_data['region']
        if region not in instances[generic['kind']]:
            instances[generic['kind']][region] = {}
        for eip_type in region_data['types'][0]['values']:
            price = eip_type['prices']['USD']
            instances[generic['kind']][region][eip_type['rate']] = price
    return instances


def process_cw(data, js_name, instances=None):
    """
    Given the JSON for the CloudWatch pricing, it loads CloudWatch pricing
    into instances dict.
    """
    generic, instances = process_generic(data, js_name, instances)
    for region_data in data['config']['regions']:
        region = region_data['region']
        if region not in instances[generic['kind']]:
            instances[generic['kind']][region] = {}
        for cw_type in region_data['types']:
            price = cw_type['values'][0]['prices']['USD']
            instances[generic['kind']][region][cw_type['name']] = price
    return instances


def process_elb(data, js_name, instances=None):
    """
    Given the JSON for the ELB pricing, it loads ELB pricing into instances
    dict.
    """
    generic, instances = process_generic(data, js_name, instances)
    for region_data in data['config']['regions']:
        region = region_data['region']
        if region not in instances[generic['kind']]:
            instances[generic['kind']][region] = {}
        for elb_type in region_data['types'][0]['values']:
            price = elb_type['prices']['USD']
            instances[generic['kind']][region][elb_type['rate']] = price
    return instances


def process_not_implemented(data, js_name, instances=None):
    """
    Given the JSON of a AWS pricing section which was not-implemented.
    """
    generic, instances = process_generic(data, js_name, instances)
    warnings.warn("WARN: Parser not implemented for {}".format(
        generic['name']))
    return instances

section_names = {
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
        'process': process_ebs,
    },
    'pricing-elastic-ips.min.js': {
        'name': 'Elastic IP Addresses',
        'key': 'ei',
        'kind': 'eip',
        'process': process_eip,
    },
    'pricing-cloudwatch.min.js': {
        'name': 'Amazon CloudWatch',
        'key': 'cw',
        'kind': 'cw',
        'process': process_cw,
    },
    'pricing-elb.min.js': {
        'name': 'Elastic Load Balancing',
        'key': 'lb',
        'kind': 'elb',
        'process': process_elb,
    },
}
