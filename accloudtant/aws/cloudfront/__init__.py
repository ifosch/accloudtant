def omit(usage_record):
    return is_data_transfer(usage_record.type) \
        or usage_record.type.endswith("Static") \
        or usage_record.type.endswith("Dynamic") \
        or usage_record.type.endswith("Bytes-HTTP-Proxy") \
        or "DataTransfer" in usage_record.type


def is_data_transfer(usage_type):
    return False


def is_bandwidth(usage_record):
    return usage_record.type.endswith("DataTransfer-Out-Bytes") \
        or usage_record.type.endswith("DataTransfer-Out-OBytes")