def omit(usage_record):
    return (
        is_data_transfer(usage_record.type)
        or usage_record.type.endswith("Static")
        or usage_record.type.endswith("Dynamic")
        or usage_record.type.endswith("Bytes-HTTPS-Proxy")
        or usage_record.type.endswith("Bytes-HTTP-Proxy")
    )


def is_data_transfer(usage_type):
    return False


def is_bandwidth(concept):
    return "DataTransfer" in concept
