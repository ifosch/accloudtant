
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


class ReservedInstance(object):
    def __init__(self, data):
        self.reserved_instance = data
        if data['State'] != 'active':
            self.instances_left = 0
        else:
            self.instances_left = self.instance_count

    @property
    def id(self):
        return self.reserved_instance['ReservedInstancesId']

    @property
    def az(self):
        return self.reserved_instance['AvailabilityZone']

    @property
    def instance_type(self):
        return self.reserved_instance['InstanceType']

    @property
    def product_description(self):
        return self.reserved_instance['ProductDescription']

    @property
    def start(self):
        return self.reserved_instance['Start']

    @property
    def end(self):
        return self.reserved_instance['End']

    @property
    def state(self):
        return self.reserved_instance['State']

    @property
    def duration(self):
        return self.reserved_instance['Duration']

    @property
    def offering_type(self):
        return self.reserved_instance['OfferingType']

    @property
    def usage_price(self):
        return self.reserved_instance['UsagePrice']

    @property
    def fixed_price(self):
        return self.reserved_instance['FixedPrice']

    @property
    def currency_code(self):
        return self.reserved_instance['CurrencyCode']

    @property
    def recurring_charges(self):
        return self.reserved_instance['RecurringCharges']

    @property
    def instance_count(self):
        return self.reserved_instance['InstanceCount']

    @property
    def instance_tenancy(self):
        return self.reserved_instance['InstanceTenancy']

    def link(self, instance):
        self.instances_left -= 1
