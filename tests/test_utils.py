import accloudtant.utils


def test_fix_lazy_json():
    bad_json = '{ key: "value" }'
    good_json = '{"key":"value"}'
    assert(accloudtant.utils.fix_lazy_json(bad_json) == good_json)
