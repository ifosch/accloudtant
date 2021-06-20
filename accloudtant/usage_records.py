from accloudtant.usage_record import SERVICES
from accloudtant.aws import unit


class UsageRecords(object):
    def __init__(self, data=None):
        if data is None:
            data = []
        self._data = data
        self.resource_areas = {}

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self._data.__iter__()

    def append(self, new):
        if new.area is not None:
            self.resource_areas[new.resource] = new.area
        self._data.append(new)

    def extend(self, other):
        for entry in other._data:
            if entry.type != "Bandwidth":
                self.append(entry)

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
            service_name = entry.service_name
            if service_name not in services:
                services[service_name] = UsageRecords()
            services[service_name].append(entry)

        return services.items()

    def totals(self):
        services = {}
        for service_name, areas in self.services():
            services[service_name] = {}
            service = SERVICES[service_name]["module"]
            for area, entries in areas.areas():
                concepts = [e.type for e in entries if not e.omit]
                services[service_name][area] = area_totals(concepts, service, entries)

        return services.items()


def area_totals(concepts, service, entries):
    area_totals = []
    for concept in set(concepts):
        total_calc = service.get_total_calc(concept)
        area_totals.append(calculate_concepts(entries, service, concept, total_calc))

    return area_totals


def calculate_concepts(entries, service, concept, total_calc_func):
    output_concept = concept
    if service.is_bandwidth(concept):
        output_concept = "Bandwidth"
    return (
        output_concept,
        "{:.3f}".format(
            total_calc_func([e for e in entries if e.type == concept and not e.omit])
        ),
        unit(concept),
    )
