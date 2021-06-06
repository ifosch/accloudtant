import argparse
from accloudtant import load_data
from accloudtant.aws import s3, data_transfer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AWS cost calculator")
    parser.add_argument("csv_file", type=str, help='CSV file to read')
    args = parser.parse_args()

    usage = load_data(args.csv_file)

    print("Simple Storage Service")
    for area, concepts in usage.totals(omit=s3.omit):
        print("\t", area)
        for c, v, u in concepts:
            print("\t\t{}\t{} {}".format(c, v, u))

    data_transfers = usage.data_transfers()
    if len(data_transfers) > 0:
        print("Data Transfer")
        for area, concepts in data_transfers.totals(omit=data_transfer.omit):
            print("\t", area)
            for c, v, u in concepts:
                print("\t\t{}\t{} {}".format(c, v, u))
