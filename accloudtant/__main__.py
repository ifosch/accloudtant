import argparse
from accloudtant import load_data
from accloudtant.aws import s3, data_transfer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AWS cost calculator")
    parser.add_argument("csv_file", type=str, help='CSV file to read')
    args = parser.parse_args()

    usage = load_data(args.csv_file)

    for service, entries in usage.services():
        print(service)
        for area, concepts in entries.totals():
            print("\t", area)
            for c, v, u in concepts:
                print("\t\t{}\t{} {}".format(c, v, u))
