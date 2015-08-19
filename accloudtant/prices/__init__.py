#!/bin/env python

from accloudtant.prices import aws

if __name__ == '__main__':
    result = aws.process_ec2()
    if result: print(result)
