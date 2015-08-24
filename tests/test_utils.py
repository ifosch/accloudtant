from accloudtant.utils import *

def test_fix_lazy_json():
    bad_json = '{ key: "value" }'
    good_json = '{"key":"value"}'
    assert(fix_lazy_json(bad_json) == good_json)
