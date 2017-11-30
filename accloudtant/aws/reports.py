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
import os
import json
import calendar
import time

class Reports(object):
    def __init__(self,output_format,region_name,save,logger=None):
        if logger is None:
            self.logger = getLogger('accloudtant.report')
            self.logger.setLevel(DEBUG)
            self.logger.addHandler(StreamHandler(sys.stdout))
        else:
            self.logger = logger
        self.output_format=output_format
        self.save=save
        #self.file_name=file_name
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
        self.prices = Prices(output_format='table',region_name='',save='no')
        self.find_reserved_instance()

    def find_reserved_instance(self):
        for instance in self.instances:
            instance_region = self.prices.prices[instance.key][instance.region]
            instance_size = instance_region[instance.size]
            try:
                instance.current = float(instance_size['od'])
            except KeyError:
                continue
            if instance.state == 'stopped':
                instance.current = 0.0
            try:
                instance_all_upfront = instance_size['ri']['yrTerm3Standard']['allUpfront']
                instance.best = float(instance_all_upfront['effectiveHourly'])
                for reserved in self.reserved_instances:
                    if instance.match_reserved_instance(reserved):
                        instance.reserved = 'Yes'
                        instance.current = reserved.usage_price
                        reserved.link(instance)
                        break
            except KeyError:
                continue
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
        if instances_counters['total'] == 0:
            reserved_counters['not reserved'] = 0
        else:
            reserved_counters['not reserved'] = instances_counters['running']
        reserved_counters['not reserved'] -= reserved_counters['used']

    def print_report(self):
        headers = [
            'Region',
            'Id',
            'Name',
            'Type',
            'AZ',
            'OS',
            'State',
            'Launch time',
            'Reserved',
            'Current\nhourly price',
            'Renewed\nhourly price',
        ]
        other_format_headers = [
            'Region',
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
                instance.region,
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
        if len(table) == 0:
            row = [os.environ['AWS_DEFAULT_REGION'],'NONE','NONE','NONE','NONE','NONE','NONE','NONE','NONE','NONE','NONE']
            table.append(row)

        if self.save != 'no':
            time_now = calendar.timegm(time.gmtime())

        if self.output_format == 'table':
            footer_headers = [
                'Running',
                'Stopped',
                'Total instances',
                'Used',
                'Free',
                'Not reserved',
                'Total reserved',
            ]
            instances_total = self.counters['instances']['total']
            if instances_total == 0:
                instances_running = 0
                instances_stopped = 0
            else:
                instances_running = self.counters['instances']['running']
                instances_stopped = self.counters['instances']['stopped']
            footer_table = [[
                instances_running,
                instances_stopped,
                instances_total,
                self.counters['reserved']['used'],
                self.counters['reserved']['free'],
                self.counters['reserved']['not reserved'],
                self.counters['reserved']['total'],
            ]]
            inventory = tabulate(table, headers,tablefmt="fancy_grid")
            summary = tabulate(footer_table, footer_headers,tablefmt="fancy_grid")
            output_message = inventory + "\n" + summary
            if self.save != 'no':
                print ('Please note table format will not be saved in any files')
            return output_message


        elif self.output_format == 'csv':
            output = ''
            for header in other_format_headers:
                output += header + ','
            output = output[:-1] + '\n'
            for row in table:
                for column in row:
                    output += str(column) + ','
                output = output[:-1] + '\n'
            if self.save != 'no':
                output_file_name = self.save + "/accloudtant-report-" + str(time_now) + "-" + table[0][0] + ".csv"
                output_file = open(output_file_name,'w')
                output_file.write(output[:-1])
                output_file.close()
                print ('The output is saved in ' + output_file_name)
            return output[:-1]

        elif self.output_format == 'json':
            json_output = "[\n{\n"
            region = table[0][0]
            json_output += '"' + region + '":{\n' + '"Instances":[\n{\n'
            number_rows = len(table)
            number_columns = len(table[0])
            row = 0
            last_column = number_columns - 1
            last_row = number_rows - 1
            while row < number_rows:
                col = 1
                while col < number_columns:
                    if col == 1:
                        json_output += '"' + str(table[row][col]) + '":{\n'
                        col += 1
                        continue
                    else:
                        json_output += '"' + other_format_headers[col] + '" : '
                    if col == last_column:
                        json_output += '"' + str(table[row][col]) + '"\n}'
                    else:
                        json_output += '"' + str(table[row][col]) + '",\n'
                    col += 1
                if row == last_row:
                    json_output += '\n}\n]\n}\n}\n]'
                else:
                    json_output += ",\n"
                row += 1
            json_output = json.loads(json_output)
            json_pretty = json.dumps(json_output,indent=4, sort_keys=True)
            if self.save != 'no':
                output_file_name = self.save + "/accloudtant-report-" + str(time_now) + "-" + region + ".json"
                output_file = open(output_file_name,'w')
                output_file.write(json_pretty)
                output_file.close()
                print ('The output is saved in ' + output_file_name)
            return json_pretty

        else:
            raise Exception()

    def __repr__(self):
        return self.print_report()
