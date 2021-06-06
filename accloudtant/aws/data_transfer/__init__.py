def omit(usage_record):
    return not usage_record.is_data_transfer


def is_data_transfer(usage_type):
    return True


def is_bandwidth(usage_record):
    return False
