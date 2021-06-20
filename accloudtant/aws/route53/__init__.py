from accloudtant.aws import default_total_calc


def omit(usage_record):
    return False


def is_data_transfer(usage_type):
    return False


def is_bandwidth(concept):
    return False


def get_total_calc(concept):
    return default_total_calc
