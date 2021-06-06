import csv

from accloudtant.usage_record import UsageRecord
from accloudtant.usage_records import UsageRecords


def load_data(csv_file):
    usage = UsageRecords()

    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            usage.append(UsageRecord(row))

    return usage


def load_files(csv_files):
    usage = UsageRecords()

    for csv_file in csv_files:
        new_usage = load_data(csv_file)
        usage.extend(new_usage)

    return usage
