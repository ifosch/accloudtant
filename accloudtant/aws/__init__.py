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
