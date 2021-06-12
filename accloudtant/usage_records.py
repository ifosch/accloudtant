from accloudtant.usage_record import SERVICES


class UsageRecords(object):
    def __init__(self, data=None):
        if data is None:
            data = []
        self._data = data
        self.resource_areas = {}

    def __getitem__(self, i):
        return self._data[i]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self._data.__iter__()

    def append(self, new):
        if new.area is not None:
            self.resource_areas[new.resource] = new.area
        self._data.append(new)

    def areas(self):
        areas = {}

        for entry in self._data:
            area_name = entry.area
            if area_name is None and entry.resource in self.resource_areas:
                area_name = self.resource_areas[entry.resource]
            if area_name not in areas:
                areas[area_name] = UsageRecords()
            areas[area_name].append(entry)

        return areas.items()

    def services(self):
        services = {}

        for entry in self._data:
            service_name = entry.service
            if service_name not in services:
                services[service_name] = UsageRecords()
            services[service_name].append(entry)

        return services.items()

    def data_transfers(self):
        return UsageRecords([entry for entry in self._data if entry.is_data_transfer])

    def totals(self):
        services = {}
        for service, areas in self.services():
            services[service] = {}
            for area, entries in areas.areas():
                services[service][area] = []
                for concept in set([entry.type for entry in entries if not entry.omit]):
                    output_concept = concept
                    total_calc = default_total_calc
                    if concept.endswith("ByteHrs"):
                        total_calc = bytehrs_total_calc
                    elif concept.endswith("Bytes"):
                        total_calc = bytes_total_calc
                    if SERVICES[service]["module"].is_bandwidth(concept):
                        output_concept = "Bandwidth"
                    services[service][area].append((
                        output_concept,
                        "{:.3f}".format(total_calc(
                            [e for e in entries if e.type == concept and not e.omit])),
                        unit(concept),
                    ))

        return services.items()


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
    elif concept.endswith("Bytes") or concept == "Bandwidth":
        return "GB"
    elif concept == "Invalidations":
        return "URL"
    elif concept == "DNS-Queries":
        return "Queries"
    elif concept == "HostedZone":
        return "Hosted zones"
    return "Requests"
