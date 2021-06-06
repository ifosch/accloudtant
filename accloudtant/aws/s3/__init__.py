def omit(usage_record):
    return usage_record.is_data_transfer or usage_record.type == "StorageObjectCount"
