import csv

from accloudtant.usage_record import UsageRecord


class UsageRecords(object):
    def __init__(self):
        self._data = []

    def __iter__(self):
        return self._data.__iter__()

    def append(self, new):
        self._data.append(new)


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
    return [entry for entry in entries if entry.is_data_transfer]


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
            if entry.value not in totals:
                totals[entry.value] = []
            totals[entry.value].append(entry)
        total = 0
        for value, values in totals.items():
            total += int(value) * len(values) / 24
        return total / 1073741824 / len(entries)
    elif entries[0].type.endswith("Bytes"):
        return sum([int(entry.value) for entry in entries]) / 1073741824
    return sum([int(entry.value) for entry in entries])


def unit(concept):
    if concept.endswith("ByteHrs"):
        return "GB-Mo"
    elif concept.endswith("Bytes"):
        return "GB"
    return "Requests"


if __name__ == "__main__":
    usage = UsageRecords()
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
        for concept, records in get_concepts(entries, omit=lambda x: x.is_data_transfer or x.type == "StorageObjectCount").items():
            total = get_total(records)
            print("\t\t", concept, "\t{:.3f}".format(total), unit(concept))

    data_transfers = get_data_transfers(usage)
    if len(data_transfers) > 0:
        print("Data Transfer")
        for area_name, entries in get_areas(data_transfers, resource_areas).items():
            print("\t", area_name)
            for concept, records in get_concepts(entries, omit=lambda x: not x.is_data_transfer).items():
                total = get_total(records)
                print("\t\t", concept, "\t{:.3f}".format(total), unit(concept))
