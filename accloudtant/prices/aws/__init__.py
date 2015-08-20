#!/bin/env python

import io
import json
import re
import warnings
import requests
from accloudtant.utils import fixLazyJson

def process_ec2():
    """
    This function drives the AWS EC2 pricing processing.
    """
    instances = {}
    pricings = requests.get('http://aws.amazon.com/ec2/pricing/')
    for html_line in io.StringIO(pricings.text):
        if 'model:' in html_line:
            url = re.sub(r".+'(.+)'.+", r"http:\1", html_line.strip())
            instances = process_model(url, instances)
    return instances

def process_model(url, instances=None):
    """
    Given the URL of a AWS JS pricing table generator, invokes the corresponding processing function according to section_names.
    """
    if instances is None:
        instances = {}
    js_name = url.split('/')[-1]
    pricing = requests.get(url)
    for js_line in io.StringIO(pricing.text.replace("\n","")):
        if 'callback' in js_line:
            data = fixLazyJson(re.sub(r".*callback\((.+)\).*", r"\1", js_line))
            instances = section_names[js_name]['process'](json.loads(data), js_name, instances)
    return instances

def process_generic(data, js_name):
    """
    Given a JSON with AWS pricing for a section, returns generic parameters.
    """
    generic = {
        'version': data['vers'],
        'rate': data['config'].get('rate'),
        'currencies': data['config']['currencies'],
        'regions': len(data['config']['regions']),
    }
    return generic

def process_on_demand(data, js_name, instances=None):
    """
    Given the JSON for the On Demand EC2 Instances AWS pricing, it loads instance attributes and On Demand pricing into instances dict.
    """
    if instances is None:
        instances = {}
    generic = process_generic(data, js_name)
    section_key = section_names[js_name]['key']
    section_kind = section_names[js_name]['kind']
    for region_data in data['config']['regions']:
        region = region_data['region']
        if region not in instances:
            instances[region] = {}
        if section_kind not in instances[region]:
            instances[region][section_kind] = {}
        section_name = "{}-{}".format(js_name, region)
        for instance_type in region_data['instanceTypes']:
            for size in instance_type.get('sizes', []):
                size_name = size['size']
                if size_name not in instances[region][section_kind]:
                    instances[region][section_kind][size_name] = {}
                instances[region][section_kind][size_name]['vCPU'] = size.get('vCPU')
                size_mem = size.get('memoryGiB')
                instances[region][section_kind][size_name]['memoryGiB'] = size_mem
                size_storage = size.get('storageGB')
                instances[region][section_kind][size_name]['storageGB'] = size_storage
                price = size['valueColumns'][0]['prices']['USD']
                instances[region][section_kind][size_name][section_key] = price
    return instances

def process_reserved(data, js_name, instances=None):
    """
    Given the JSON for the Reserved EC2 Instances AWS pricing, it loads Reserved pricing into instances dict.
    """
    if instances is None:
        instances = {}
    generic = process_generic(data, js_name)
    section_key = section_names[js_name]['key']
    section_kind = section_names[js_name]['kind']
    for region_data in data['config']['regions']:
        region = region_data['region']
        if region not in instances:
            instances[region] = {}
        if section_kind not in instances[region]:
            instances[region][section_kind] = {}
        section_name = "{}-{}".format(js_name, region)
        for instance_type in region_data['instanceTypes']:
            size_name = instance_type['type']
            if size_name not in instances[region][section_kind]:
                instances[region][size_name] = {}
                instances[region][section_kind][size_name] = {}
            instances[region][section_kind][size_name][section_key] = {}
            for term in instance_type['terms']:
                term_name = term['term']
                if 'ri' not in instances[region][section_kind][size_name]:
                    instances[region][section_kind][size_name]['ri'] = {}
                if term_name not in instances[region][section_kind][size_name]['ri']:
                    instances[region][section_kind][size_name]['ri'][term_name] = {}
                for purchase_option in term['purchaseOptions']:
                    po_name = purchase_option['purchaseOption']
                    prices = {}
                    for value in purchase_option['valueColumns']:
                        prices[value['name']] = value['prices']['USD']
                    instances[region][section_kind][size_name]['ri'][term_name][po_name] = prices
    return instances

def process_data_transfer(data, js_name, instances=None):
    """
    Given the JSON for the Data Transfer pricing, it loads Data Transfer pricing into instances dict.
    """
    if instances is None:
        instance = {}
    generic = process_generic(data, js_name)
    section_key = section_names[js_name]['key']
    section_kind = section_names[js_name]['kind']
    for region_data in data['config']['regions']:
        region = region_data['region']
        if region not in instances:
            instances[region] = {}
        if section_kind not in instances:
            instances[region][section_kind] = {}
        instances[region][section_kind]['regional'] = region_data['regionalDataTransfer']
        instances[region][section_kind]['ELB'] = region_data['elasticLBDataTransfer']
        instances[region][section_kind]['AZ'] = region_data['azDataTransfer']
        for dt_type in region_data['types']:
            type_name = dt_type['name']
            if type_name not in instances[region][section_kind]: instances[region][section_kind][type_name] = {}
            for dt_tier in dt_type['tiers']:
                price = dt_tier['prices']['USD']
                if len(price): instances[region][section_kind][type_name][dt_tier['name']] = price
    return instances

def process_ebs(data, js_name, instances=None):
    """
    Given the JSON for the EBS pricing, it loads EBS pricing into instances dict.
    """
    if instances is None:
        instances = {}
    generic = process_generic(data, js_name)
    section_key = section_names[js_name]['key']
    section_kind = section_names[js_name]['kind']
    for region_data in data['config']['regions']:
        region = region_data['region']
        if region not in instances:
            instances[region] = {}
        if section_kind not in instances[region]:
            instances[region][section_kind] = {}
        for ebs_type in region_data['types']:
            price = ebs_type['values'][0]['prices']['USD']
            instances[region][section_kind][ebs_type['name']] = price
    return instances

def process_not_implemented(data, js_name, instances=None):
    """
    Given the JSON of a AWS pricing section which was not-implemented.
    """
    section_kind = section_names[js_name]['kind']
    section_name = section_names[js_name]['name']
    warnings.warn("WARN: Parser not implemented for {} {}".format(section_kind, section_name))

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
        'kind': 'other',
        'process': process_not_implemented,
    },
    'pricing-cloudwatch.min.js': {
        'name': 'Amazon CloudWatch',
        'key': 'cw',
        'kind': 'other',
        'process': process_not_implemented,
    },
    'pricing-elb.min.js': {
        'name': 'Elastic Load Balancing',
        'key': 'lb',
        'kind': 'other',
        'process': process_not_implemented,
    },
}
