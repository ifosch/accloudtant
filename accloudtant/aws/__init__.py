#!/bin/env python

import warnings
from accloudtant.aws import prices

if __name__ == '__main__':
    with warnings.catch_warnings(record=True) as w:
        result = prices.process_ec2()
        for warning in w:
            print(warning.message)
