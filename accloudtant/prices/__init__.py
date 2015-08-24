#!/bin/env python

import warnings
from accloudtant.prices import aws

if __name__ == '__main__':
    with warnings.catch_warnings(record=True) as w:
      result = aws.process_ec2()
      for warning in w:
          print(warning.message)
