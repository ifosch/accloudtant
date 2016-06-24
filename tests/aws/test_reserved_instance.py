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

import datetime
import pytest
from dateutil.tz import tzutc
import accloudtant.aws.reserved_instance


def test_reserved_instance():
    az = 'us-east-1b'
    region = 'us-east-1'
    ri_data = {
        'ProductDescription': 'Linux/UNIX',
        'InstanceTenancy': 'default',
        'InstanceCount': 29,
        'InstanceType': 'm1.large',
        'Start': datetime.datetime(
                2011,
                6,
                5,
                6,
                20,
                10,
                494000,
                tzinfo=tzutc()
            ),
        'RecurringCharges': [],
        'End': datetime.datetime(
                2011,
                6,
                5,
                6,
                20,
                10,
                tzinfo=tzutc()
            ),
        'CurrencyCode': 'USD',
        'OfferingType': 'Medium Utilization',
        'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df1223331f',
        'FixedPrice': 910.0,
        'AvailabilityZone': 'us-east-1c',
        'UsagePrice': 0.12,
        'Duration': 31536000,
        'State': 'retired',
    }

    ri = accloudtant.aws.reserved_instance.ReservedInstance(
        ri_data)

    assert(ri.id == ri_data['ReservedInstancesId'])
    assert(ri.product_description == ri_data['ProductDescription'])
    assert(ri.instance_tenancy == ri_data['InstanceTenancy'])
    assert(ri.instance_count == ri_data['InstanceCount'])
    assert(ri.instance_type == ri_data['InstanceType'])
    assert(ri.start == ri_data['Start'])
    assert(ri.recurring_charges == ri_data['RecurringCharges'])
    assert(ri.end == ri_data['End'])
    assert(ri.currency_code == ri_data['CurrencyCode'])
    assert(ri.offering_type == ri_data['OfferingType'])
    assert(ri.fixed_price == ri_data['FixedPrice'])
    assert(ri.az == ri_data['AvailabilityZone'])
    assert(ri.usage_price == ri_data['UsagePrice'])
    assert(ri.duration == ri_data['Duration'])
    assert(ri.state == ri_data['State'])
