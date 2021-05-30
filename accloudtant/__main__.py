import csv

from accloudtant.usage_record import UsageRecord
from accloudtant.usage_records import UsageRecords


if __name__ == "__main__":
    usage = UsageRecords()

    with open("tests/fixtures/2021/03/S3.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            usage.append(UsageRecord(row))

    print("Simple Storage Service")
    for area, concepts in usage.totals(omit=lambda x: x.is_data_transfer or x.type == "StorageObjectCount"):
        print("\t", area)
        for c, v, u in concepts:
            print("\t\t{}\t{} {}".format(c, v, u))

    data_transfers = usage.data_transfers()
    if len(data_transfers) > 0:
        print("Data Transfer")
        for area, concepts in data_transfers.totals(omit=lambda x: not x.is_data_transfer):
            print("\t", area)
            for c, v, u in concepts:
                print("\t\t{}\t{} {}".format(c, v, u))
