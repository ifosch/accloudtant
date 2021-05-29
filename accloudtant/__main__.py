import csv


def area(entry):
    if entry[" UsageType"].startswith("EUC1-"):
        return "EU (Frankfurt)"


if __name__ == "__main__":
    usage = []

    with open("tests/fixtures/2021/03/S3.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            usage.append(row)

    print("Simple Storage Service")
    for area_name in set([area(entry) for entry in usage]):
        print("\t", area_name)
