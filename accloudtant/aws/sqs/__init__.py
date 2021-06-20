from accloudtant.aws import default_total_calc, UNITS_PER_CONCEPT


def omit(usage_record):
    return "C3DataTransfer" in usage_record.type


def is_data_transfer(usage_type):
    return False


def is_bandwidth(concept):
    return False


def get_total_calc(concept):
    return default_total_calc
