#!/usr/bin/env python
import boto3
from tabulate import tabulate


class Reports(object):
    def __init__(self):
        ec2 = boto3.resource('ec2')
        self.instances = list(ec2.instances.all())
        self.set_billing_os()
        ec2_client = boto3.client('ec2')
        self.reservations = ec2_client.describe_instances()
        self.reserved_instances = {}
        self.get_reservations_info()

    def set_billing_os(self):
        self.billing_os = {}
        for instance in self.instances:
            self.billing_os[instance.id] = self.guess_os(instance)

    def guess_os(self, instance):
        console_output = instance.console_output()['Output']
        if 'Windows' in console_output:
            return ('Windows', 'win')
        else:
            if 'RHEL' in console_output:
                return ('Red Hat Enterprise Linux', 'rhel')
            elif 'SUSE' in console_output:
                return ('SUSE Linux', 'suse')
            else:
                return ('Linux/UNIX', 'linux')

    def get_name(self, instance):
        names = [tag for tag in instance.tags if tag['Key'] == 'Name']
        if names is None:
            return ''
        else:
            return names[0]['Value']

    def get_reservations_info(self):
        for instance in self.instances:
            self.reserved_instances[instance.id] = '-'
            for reservation in self.reservations['Reservations']:
                reservation_id = reservation['ReservationId']
                for reserved_instance in reservation['Instances']:
                    if instance.id == reserved_instance['InstanceId']:
                        self.reserved_instances[instance.id] = reservation_id

    def __repr__(self):
        headers = [
                'Id',
                'Name',
                'Type',
                'AZ',
                'OS',
                'State',
                'Launch time',
                'Reservation Id',
                ]
        table = []
        for instance in self.instances:
            row = [
                    instance.id,
                    self.get_name(instance),
                    instance.instance_type,
                    instance.placement['AvailabilityZone'],
                    self.billing_os[instance.id][0],
                    instance.state['Name'],
                    instance.launch_time.strftime('%Y-%m-%d %H:%M:%S'),
                    self.reserved_instances[instance.id],
                    ]
            table.append(row)
        return tabulate(table, headers)
