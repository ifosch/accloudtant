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

import codecs
import accloudtant.utils


def test_fix_lazy_json():
    bad_json = '{ key: "value" }'.encode('utf-8')
    good_json = '{"key":"value"}'
    assert(accloudtant.utils.fix_lazy_json(codecs.decode(bad_json)) == good_json)
