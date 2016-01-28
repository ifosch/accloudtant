#!/usr/bin/env python
import boto3
from tabulate import tabulate
from accloudtant.aws.instance import Instance
from accloudtant.aws.prices import Prices


class Reports(object):
    def __init__(self):
        ec2 = boto3.resource('ec2')
        self.instances = [Instance(i) for i in ec2.instances.all()]
        ec2_client = boto3.client('ec2')
        self.reserved_instances = ec2_client.describe_reserved_instances()
        self.prices = Prices()
        self.find_reserved_instance()

    def find_reserved_instance(self):
        for instance in self.instances:
            instance.current = float(self.prices.prices[instance.key][instance.region][instance.size]['od'])
            if instance.state == 'stopped':
                instance.current = 0.0
            instance.best = float(self.prices.prices[instance.key][instance.region][instance.size]['ri']['yrTerm3']['allUpfront']['effectiveHourly'])
            for reserved in self.reserved_instances['ReservedInstances']:
                    if 'InstancesLeft' not in reserved.keys():
                        reserved['InstancesLeft'] = reserved['InstanceCount']
                    if instance.match_reserved_instance(reserved):
                        instance._reserved = True
                        instance.current = reserved['UsagePrice']
                        reserved['InstancesLeft'] -= 1
                        break

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
                    ]
            table.append(row)
        return tabulate(table, headers)
