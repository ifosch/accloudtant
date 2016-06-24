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


class Instance(object):
    def __init__(self, obj):
        self.id = obj.id
        self.tags = obj.tags
        self.size = obj.instance_type
        self.launch_time = obj.launch_time
        self._placement = obj.placement
        self._state = obj.state
        self._os = guess_os(obj)
        self._reserved = False
        self._prices = {
            'current': 0.0,
            'best': 0.0,
        }

    def __repr__(self):
        return "<accloudtant.aws.instance.Instance id={}>".format(self.id)

    @property
    def current(self):
        return self._prices['current']

    @current.setter
    def current(self, value):
        self._prices['current'] = value

    @property
    def best(self):
        return self._prices['best']

    @best.setter
    def best(self, value):
        self._prices['best'] = value

    @property
    def reserved(self):
        if self._reserved:
            return 'Yes'
        else:
            return 'No'

    @reserved.setter
    def reserved(self, value):
        if value == 'Yes':
            self._reserved = True
        elif value == 'No':
            self._reserved = False
        else:
            raise ValueError

    @property
    def name(self):
        names = [tag for tag in self.tags if tag['Key'] == 'Name']
        if len(names) == 0:
            return ''
        else:
            return names[0]['Value']

    @property
    def availability_zone(self):
        return self._placement['AvailabilityZone']

    @property
    def region(self):
        return self._placement['AvailabilityZone'][:-1]

    @property
    def key(self):
        return self._os[1]

    @property
    def operating_system(self):
        return self._os[0]

    @property
    def state(self):
        return self._state['Name']

    def match_reserved_instance(self, reserved):
        return not (
           self.state != 'running' or
           reserved.state != 'active' or
           reserved.instances_left == 0 or
           reserved.product_description != self.operating_system or
           reserved.instance_type != self.size or
           reserved.az != self.availability_zone
        )


def guess_os(instance):
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
