def omit(usage_record):
    return is_data_transfer(usage_record.type) or usage_record.type == "StorageObjectCount"


def is_data_transfer(usage_type):
    return "DataTransfer" in usage_type or "CloudFront" in usage_type
