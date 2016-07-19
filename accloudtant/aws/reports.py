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

from logging import getLogger, StreamHandler, DEBUG
import boto3
from botocore import exceptions
from tabulate import tabulate
from accloudtant.aws.instance import Instance
from accloudtant.aws.reserved_instance import ReservedInstance
from accloudtant.aws.prices import Prices
import sys


class Reports(object):
    def __init__(self, logger=None):
        if logger is None:
            self.logger = getLogger('accloudtant.report')
            self.logger.setLevel(DEBUG)
            self.logger.addHandler(StreamHandler(sys.stdout))
        else:
            self.logger = logger
        ec2 = boto3.resource('ec2')
        ec2_client = boto3.client('ec2')
        self.counters = {
            'instances': {
                'total': 0,
            },
            'reserved': {
                'total': 0,
            },
        }
        self.instances = []
        self.reserved_instances = []
        try:
            for i in ec2.instances.all():
                instance = Instance(i)
                if instance.state == "running":
                    self.instances.append(instance)
                if instance.state not in self.counters['instances']:
                    self.counters['instances'][instance.state] = 0
                self.counters['instances'][instance.state] += 1
                self.counters['instances']['total'] += 1
            ri_key = 'ReservedInstances'
            reserved_ctrs = self.counters['reserved']
            for r in ec2_client.describe_reserved_instances()[ri_key]:
                reserved_instance = ReservedInstance(r)
                if reserved_instance.state == "active":
                    self.reserved_instances.append(reserved_instance)
                    reserved_ctrs['total'] += reserved_instance.instance_count
            reserved_ctrs['free'] = reserved_ctrs['total']
            reserved_ctrs['not_reserved'] = reserved_ctrs['total']
            reserved_ctrs['used'] = 0
            reserved_ctrs['not reserved'] = 0
        except exceptions.NoCredentialsError:
            logger.error("Error: no AWS credentials found")
            sys.exit(1)
        self.prices = Prices()
        self.find_reserved_instance()

    def find_reserved_instance(self):
        for instance in self.instances:
            instance_region = self.prices.prices[instance.key][instance.region]
            instance_size = instance_region[instance.size]
            instance.current = float(instance_size['od'])
            if instance.state == 'stopped':
                instance.current = 0.0
            instance_all_upfront = instance_size['ri']['yrTerm3']['allUpfront']
            instance.best = float(instance_all_upfront['effectiveHourly'])
            for reserved in self.reserved_instances:
                if instance.match_reserved_instance(reserved):
                    instance.reserved = 'Yes'
                    instance.current = reserved.usage_price
                    reserved.link(instance)
                    self.counters['reserved']['used'] += 1
                    self.counters['reserved']['free'] -= 1
                    break
        reserved_counters = self.counters['reserved']
        instances_counters = self.counters['instances']
        reserved_counters['not reserved'] = instances_counters['running']
        reserved_counters['not reserved'] -= reserved_counters['used']

    def __repr__(self):
        headers = [
            'Id',
            'Name',
            'Type',
            'AZ',
            'OS',
            'State',
            'Launch time',
            'Reserved',
            'Current hourly price',
            'Renewed hourly price',
        ]
        table = []
        for instance in self.instances:
            row = [
                instance.id,
                instance.name,
                instance.size,
                instance.availability_zone,
                instance.operating_system,
                instance.state,
                instance.launch_time.strftime('%Y-%m-%d %H:%M:%S'),
                instance.reserved,
                instance.current,
                instance.best,
            ]
            table.append(row)
        footer_headers = [
            'Running',
            'Stopped',
            'Total instances',
            'Used',
            'Free',
            'Not reserved',
            'Total reserved',
        ]
        footer_table = [[
            self.counters['instances']['running'],
            self.counters['instances']['stopped'],
            self.counters['instances']['total'],
            self.counters['reserved']['used'],
            self.counters['reserved']['free'],
            self.counters['reserved']['not reserved'],
            self.counters['reserved']['total'],
        ]]
        inventory = tabulate(table, headers)
        summary = tabulate(footer_table, footer_headers)
        return "{}\n\n{}".format(inventory, summary)
