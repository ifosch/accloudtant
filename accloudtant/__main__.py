import csv


def area(entry):
    if entry[" UsageType"].startswith("EUC1-"):
        return "EU (Frankfurt)"


def is_data_transfer(entry):
    if "DataTransfer" in entry[" UsageType"] or "CloudFront" in entry[" UsageType"]:
        return True
    return False


def omit(entry):
    if is_data_transfer(entry) or entry[" UsageType"] == "StorageObjectCount":
        return True
    return False


def get_areas(entries, resource_areas):
    areas = {}

    for entry in entries:
        area_name = area(entry)
        if area_name is None and entry[" Resource"] in resource_areas:
            area_name = resource_areas[entry[" Resource"]]
        if area_name not in areas:
            areas[area_name] = []
        areas[area_name].append(entry)

    return areas


def get_concepts(entries):
    concepts = {}

    for entry in entries:
        if not omit(entry):
            if entry[" UsageType"] not in concepts:
                concepts[entry[" UsageType"]] = []
            concepts[entry[" UsageType"]].append(entry)

    return concepts


if __name__ == "__main__":
    usage = []
    resource_areas = {}

    with open("tests/fixtures/2021/03/S3.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            usage.append(row)
            if area(row) is not None:
                resource_areas[row[" Resource"]] = area(row)

    print("Simple Storage Service")
    for area_name, entries in get_areas(usage, resource_areas).items():
        print("\t", area_name)
        for concept, records in get_concepts(entries).items():
            total = sum([int(record[" UsageValue"]) for record in records])
            print("\t\t", concept, "\t", total)
