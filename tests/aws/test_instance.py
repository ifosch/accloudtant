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
from dateutil.tz import tzutc
import accloudtant.aws.instance
from conftest import MockEC2Instance


def test_instance():
    az = 'us-east-1b'
    region = 'us-east-1'
    instance_data = {
        'id': 'i-1840273e',
        'tags': [{
            'Key': 'Name',
            'Value': 'app1',
        }, ],
        'instance_type': 'r2.8xlarge',
        'placement': {
            'AvailabilityZone': az,
        },
        'state': {
            'Name': 'running',
        },
        'launch_time': datetime.datetime(
                2015,
                10,
                22,
                14,
                15,
                10,
                tzinfo=tzutc()
            ),
        'console_output': {'Output': 'RHEL Linux', },
    }

    ec2_instance = MockEC2Instance(instance_data)
    instance = accloudtant.aws.instance.Instance(ec2_instance)

    assert(instance.id == ec2_instance.id)
    assert(instance.reserved == 'No')
    assert(instance.name == ec2_instance.tags[0]['Value'])
    assert(instance.size == ec2_instance.instance_type)
    assert(instance.availability_zone == az)
    assert(instance.region == region)
    assert(instance.operating_system == 'Red Hat Enterprise Linux')
    assert(instance.key == 'rhel')
    assert(instance.state == ec2_instance.state['Name'])
    assert(instance.current == 0.0)
    assert(instance.best == 0.0)

    instance.current = 0.392
    instance.best = 0.293

    assert(instance.current == 0.392)
    assert(instance.best == 0.293)


def test_guess_os():
    instance_data_win = {
            'id': 'i-912a4392',
            'tags': [{
                'Key': 'Name',
                'Value': 'web1',
            }, ],
            'instance_type': 'c3.8xlarge',
            'placement': {
                'AvailabilityZone': 'us-east-1c',
            },
            'state': {
                'Name': 'running',
            },
            'launch_time': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc(),
                ),
            'console_output': {'Output': 'Windows', },
    }
    instance_data_rhel = {
            'id': 'i-1840273e',
            'tags': [{
                'Key': 'Name',
                'Value': 'app1',
            }, ],
            'instance_type': 'r2.8xlarge',
            'placement': {
                'AvailabilityZone': 'us-east-1b',
            },
            'state': {
                'Name': 'running',
            },
            'launch_time': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc()
                ),
            'console_output': {'Output': 'RHEL Linux', },
    }
    instance_data_sles = {
            'id': 'i-9840273d',
            'tags': [{
                'Key': 'Name',
                'Value': 'app2',
            }, ],
            'instance_type': 'r2.8xlarge',
            'placement': {
                'AvailabilityZone': 'us-east-1c',
            },
            'state': {
                'Name': 'stopped',
            },
            'launch_time': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc()
                ),
            'console_output': {'Output': 'SUSE Linux', },
    }
    instance_data_linux = {
            'id': 'i-1840273c',
            'tags': [{
                'Key': 'Name',
                'Value': 'database2',
            }, ],
            'instance_type': 'r2.8xlarge',
            'placement': {
                'AvailabilityZone': 'us-east-1c',
            },
            'state': {
                'Name': 'running',
            },
            'launch_time': datetime.datetime(
                    2015,
                    10,
                    22,
                    14,
                    15,
                    10,
                    tzinfo=tzutc()
                ),
            'console_output': {'Output': 'Linux', },
    }

    ec2_instance_win = MockEC2Instance(instance_data_win)
    ec2_instance_rhel = MockEC2Instance(instance_data_rhel)
    ec2_instance_sles = MockEC2Instance(instance_data_sles)
    ec2_instance_linux = MockEC2Instance(instance_data_linux)
    instance_win = accloudtant.aws.instance.Instance(ec2_instance_win)
    instance_rhel = accloudtant.aws.instance.Instance(ec2_instance_rhel)
    instance_sles = accloudtant.aws.instance.Instance(ec2_instance_sles)
    instance_linux = accloudtant.aws.instance.Instance(ec2_instance_linux)

    assert(instance_win.operating_system == 'Windows')
    assert(instance_rhel.operating_system == 'Red Hat Enterprise Linux')
    assert(instance_sles.operating_system == 'SUSE Linux')
    assert(instance_linux.operating_system == 'Linux/UNIX')


def test_match_reserved_instance():
    az = 'us-east-1b'
    instance_data = {
        'id': 'i-1840273e',
        'tags': [{
            'Key': 'Name',
            'Value': 'app1',
        }, ],
        'instance_type': 'r2.8xlarge',
        'placement': {
            'AvailabilityZone': az,
        },
        'state': {
            'Name': 'running',
        },
        'launch_time': datetime.datetime(
                2015,
                10,
                22,
                14,
                15,
                10,
                tzinfo=tzutc()
            ),
        'console_output': {'Output': 'RHEL Linux', },
    }
    reserved_instance = {
        'ProductDescription': 'Red Hat Enterprise Linux',
        'InstanceTenancy': 'default',
        'InstanceCount': 1,
        'InstanceType': 'r2.8xlarge',
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
        'ReservedInstancesId': '46a408c7-c33d-422d-af59-28df12233321',
        'FixedPrice': 910.0,
        'AvailabilityZone': 'us-east-1b',
        'UsagePrice': 0.12,
        'Duration': 31536000,
        'State': 'active',
    }

    ec2_instance = MockEC2Instance(instance_data)
    instance = accloudtant.aws.instance.Instance(ec2_instance)
    reserved_instance['InstancesLeft'] = reserved_instance['InstanceCount']

    assert(instance.match_reserved_instance(reserved_instance))

    reserved_instance['State'] = 'pending'

    assert(not instance.match_reserved_instance(reserved_instance))

    reserved_instance['State'] = 'active'
    reserved_instance['InstancesLeft'] = 0

    assert(not instance.match_reserved_instance(reserved_instance))

    reserved_instance['InstacesLeft'] = 1
    reserved_instance['ProductDescription'] = 'Windows'

    assert(not instance.match_reserved_instance(reserved_instance))

    reserved_instance['ProductionDescription'] = 'Red Hat Enterprise Linux'
    reserved_instance['InstaceType'] = 't1.micro'

    assert(not instance.match_reserved_instance(reserved_instance))

    reserved_instance['InstaceType'] = 'r2.8xlarge'
    reserved_instance['AvailabilityZone'] = 'us-east-1c'

    assert(not instance.match_reserved_instance(reserved_instance))
