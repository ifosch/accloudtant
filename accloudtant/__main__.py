import csv


class UsageRecord(object):
    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

    @property
    def type(self):
        return self._data[" UsageType"]

    @property
    def resource(self):
        return self._data[" Resource"]

    @property
    def area(self):
        if self.type.startswith("EUC1-"):
            return "EU (Frankfurt)"


def is_data_transfer(entry):
    if "DataTransfer" in entry.type or "CloudFront" in entry.type:
        return True
    return False


def get_areas(entries, resource_areas):
    areas = {}

    for entry in entries:
        area_name = entry.area
        if area_name is None and entry.resource in resource_areas:
            area_name = resource_areas[entry.resource]
        if area_name not in areas:
            areas[area_name] = []
        areas[area_name].append(entry)

    return areas


def get_data_transfers(entries):
    return [entry for entry in entries if is_data_transfer(entry)]


def get_concepts(entries, omit=lambda x: False):
    concepts = {}

    for entry in entries:
        if not omit(entry):
            if entry.type not in concepts:
                concepts[entry.type] = []
            concepts[entry.type].append(entry)

    return concepts


def get_total(entries):
    if entries[0].type.endswith("ByteHrs"):
        totals = {}
        for entry in entries:
            if entry[" UsageValue"] not in totals:
                totals[entry[" UsageValue"]] = []
            totals[entry[" UsageValue"]].append(entry)
        total = 0
        for value, values in totals.items():
            total += int(value) * len(values) / 24
        return total / 1073741824 / len(entries)
    elif entries[0].type.endswith("Bytes"):
        return sum([int(entry[" UsageValue"]) for entry in entries]) / 1073741824
    return sum([int(entry[" UsageValue"]) for entry in entries])


def unit(concept):
    if concept.endswith("ByteHrs"):
        return "GB-Mo"
    elif concept.endswith("Bytes"):
        return "GB"
    return "Requests"


if __name__ == "__main__":
    usage = []
    resource_areas = {}

    with open("tests/fixtures/2021/03/S3.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entry = UsageRecord(row)
            usage.append(entry)
            if entry.area is not None:
                resource_areas[entry.resource] = entry.area

    print("Simple Storage Service")
    for area_name, entries in get_areas(usage, resource_areas).items():
        print("\t", area_name)
        for concept, records in get_concepts(entries, omit=lambda x: is_data_transfer(x) or x.type == "StorageObjectCount").items():
            total = get_total(records)
            print("\t\t", concept, "\t{:.3f}".format(total), unit(concept))

    data_transfers = get_data_transfers(usage)
    if len(data_transfers) > 0:
        print("Data Transfer")
        for area_name, entries in get_areas(data_transfers, resource_areas).items():
            print("\t", area_name)
            for concept, records in get_concepts(entries, omit=lambda x: not is_data_transfer(x)).items():
                total = get_total(records)
                print("\t\t", concept, "\t{:.3f}".format(total), unit(concept))
