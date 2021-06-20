from accloudtant.aws import default_total_calc, bytehrs_total_calc, bytes_total_calc


def omit(usage_record):
    return (
        is_data_transfer(usage_record.type) or usage_record.type == "StorageObjectCount"
    )


def is_data_transfer(usage_type):
    return "DataTransfer" in usage_type or "CloudFront" in usage_type


def is_bandwidth(concept):
    return False


def get_total_calc(concept):
    if concept.endswith("ByteHrs"):
        return bytehrs_total_calc
    return default_total_calc
