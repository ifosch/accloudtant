import csv


def area(entry):
    if entry[" UsageType"].startswith("EUC1-"):
        return "EU (Frankfurt)"


def get_areas(entries):
    areas = {}

    for entry in entries:
        area_name = area(entry)
        if area_name not in areas:
            areas[area_name] = []
        areas[area_name].append(entry)

    return areas


if __name__ == "__main__":
    usage = []

    with open("tests/fixtures/2021/03/S3.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            usage.append(row)

    print("Simple Storage Service")
    for area_name, entries in get_areas(usage).items():
        print("\t", area_name)
        for concept in set([entry[" UsageType"] for entry in entries]):
            print("\t\t", concept)
