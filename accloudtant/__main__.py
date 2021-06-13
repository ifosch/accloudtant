import argparse
from accloudtant import load_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AWS cost calculator")
    parser.add_argument(
        "csv_files",
        type=str,
        nargs="*",
        help="CSV file to read",
    )
    args = parser.parse_args()

    usage = load_files(args.csv_files)

    for service, areas in usage.totals():
        print(service)
        for area, concepts in areas.items():
            print("\t", area)
            for c, v, u in concepts:
                print("\t\t{}\t{} {}".format(c, v, u))
