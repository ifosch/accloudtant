from accloudtant.aws import s3, cloudfront, data_transfer, route53

SERVICES = {
    "AmazonS3": {
        "name": "Simple Storage Service",
        "module": s3,
    },
    "AmazonCloudFront": {
        "name": "CloudFront",
        "module": cloudfront,
    },
    "AmazonRoute53": {
        "name": "Route 53",
        "module": route53,
    },
    "Data Transfer": {
        "name": "Data Transfer",
        "module": data_transfer,
    },
}


class UsageRecord(object):
    def __init__(self, data):
        self._data = data

    @property
    def service_name(self):
        if SERVICES[self._data["Service"]]["module"].is_data_transfer(self.type):
            return "Data Transfer"
        return self._data["Service"]

    @property
    def service(self):
        if self.service_name in SERVICES:
            return SERVICES[self.service_name]["module"]
        return None

    @property
    def type(self):
        return self._data[" UsageType"]

    @property
    def value(self):
        return int(self._data[" UsageValue"])

    @property
    def resource(self):
        return self._data[" Resource"]

    @property
    def area(self):
        if self.type.startswith("EUC1-"):
            return "EU (Frankfurt)"
        elif self.type.startswith("US-"):
            return "United States"
        elif self.type.startswith("EU-"):
            return "Europe"
        elif self.type.startswith("CA-"):
            return "Canada"
        elif self.type == "Invalidations" or self.service_name == "AmazonRoute53":
            return "Global"

    @property
    def is_data_transfer(self):
        return self.service.is_data_transfer(self.type)

    @property
    def omit(self):
        return self.service.omit(self)
