#!/usr/bin/env python
import boto3


class Reports(object):
    def __init__(self):
        ec2 = boto3.resource('ec2')
        self.instances = list(ec2.instances.all())
