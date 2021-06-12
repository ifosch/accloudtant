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
    def service(self):
        if SERVICES[self._data["Service"]]["module"].is_data_transfer(self.type):
            return "Data Transfer"
        return self._data["Service"]

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
        elif self.type == "Invalidations" or self.service == "AmazonRoute53":
            return "Global"

    @property
    def is_data_transfer(self):
        if self.service in SERVICES:
            return SERVICES[self.service]["module"].is_data_transfer(self.type)
        return False

    @property
    def omit(self):
        if self.service in SERVICES:
            return SERVICES[self.service]["module"].omit(self)
        return False

    @property
    def is_bandwidth(self):
        if self.service in SERVICES:
            return SERVICES[self.service]["module"].is_bandwidth(self)
        return False
