import csv

from accloudtant.usage_record import UsageRecord


class UsageRecords(object):
    def __init__(self, data=None):
        if data is None:
            data = []
        self._data = data

    def __getitem__(self, i):
        return self._data[i]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self._data.__iter__()

    def append(self, new):
        self._data.append(new)

    def areas(self, resource_areas):
        areas = {}

        for entry in self._data:
            area_name = entry.area
            if area_name is None and entry.resource in resource_areas:
                area_name = resource_areas[entry.resource]
            if area_name not in areas:
                areas[area_name] = UsageRecords()
            areas[area_name].append(entry)

        return areas.items()

    def data_transfers(self):
        return UsageRecords([entry for entry in self._data if entry.is_data_transfer])

    def totals(self, omit=lambda x: False):
        concepts = []

        for concept in set([entry.type for entry in self._data if not omit(entry)]):
            total_calc = default_total_calc
            if concept.endswith("ByteHrs"):
                total_calc = bytehrs_total_calc
            elif concept.endswith("Bytes"):
                total_calc = bytes_total_calc
            concepts.append((
                concept,
                "{:.3f}".format(total_calc(
                    [e for e in self._data if e.type == concept and not omit(e)])),
                unit(concept),
            ))

        return concepts


def default_total_calc(entries):
    return sum([int(entry.value) for entry in entries])


def bytes_total_calc(entries):
    return default_total_calc(entries) / 1073741824


def bytehrs_total_calc(entries):
    totals = {}
    for entry in entries:
        if entry.value not in totals:
            totals[entry.value] = []
        totals[entry.value].append(entry)
    total = 0
    for value, values in totals.items():
        total += int(value) * len(values) / 24
    return total / 1073741824 / len(entries)


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
    for area_name, entries in usage.areas(resource_areas):
        print("\t", area_name)
        for concept, value, u in entries.totals(
                omit=lambda x: x.is_data_transfer or x.type == "StorageObjectCount"):
            print("\t\t{}\t{} {}".format(concept, value, u))

    data_transfers = usage.data_transfers()
    if len(data_transfers) > 0:
        print("Data Transfer")
        for area_name, entries in data_transfers.areas(resource_areas):
            print("\t", area_name)
            for concept, value, u in entries.totals(
                    omit=lambda x: not x.is_data_transfer):
                print("\t\t{}\t{} {}".format(concept, value, u))
