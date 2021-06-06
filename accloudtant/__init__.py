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
