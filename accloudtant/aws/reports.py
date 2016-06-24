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

import boto3
from botocore import exceptions
from tabulate import tabulate
from accloudtant.aws.instance import Instance
from accloudtant.aws.reserved_instance import ReservedInstance
from accloudtant.aws.prices import Prices
import sys


class Reports(object):
    def __init__(self):
        ec2 = boto3.resource('ec2')
        ec2_client = boto3.client('ec2')
        instances_filters = [{
            'Name': 'instance-state-name',
            'Values': ['running', ],
        }, ]
        reserved_instances_filters = [{
            'Name': 'state',
            'Values': ['active', ],
        }, ]
        try:
            self.instances = [
                Instance(i)
                for i in ec2.instances.filter(Filters=instances_filters)
            ]
            # self.instances = [Instance(i) for i in ec2.instances.all()]
            self.reserved_instances = [
                ReservedInstance(i)
                for i in ec2_client.describe_reserved_instances(
                    Filters=reserved_instances_filters
                )['ReservedInstances']
            ]
            # self.reserved_instances = ec2_client
            # .describe_reserved_instances()
        except exceptions.NoCredentialsError:
            print("Error: no AWS credentials found", file=sys.stderr)
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
                    break

    def __repr__(self):
        headers = ['Id',
                   'Name',
                   'Type',
                   'AZ',
                   'OS',
                   'State',
                   'Launch time',
                   'Reserved',
                   'Current hourly price',
                   'Renewed hourly price']
        table = []
        for instance in self.instances:
            row = [instance.id,
                   instance.name,
                   instance.size,
                   instance.availability_zone,
                   instance.operating_system,
                   instance.state,
                   instance.launch_time.strftime('%Y-%m-%d %H:%M:%S'),
                   instance.reserved,
                   instance.current,
                   instance.best]
            table.append(row)
        return tabulate(table, headers)
