from accloudtant.aws import s3, data_transfer

SERVICES = {
    "AmazonS3": {
        "name": "Simple Storage Service",
        "module": s3,
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
        if self.is_data_transfer:
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

    @property
    def is_data_transfer(self):
        return "DataTransfer" in self.type or "CloudFront" in self.type

    @property
    def omit(self):
        if self.service in SERVICES:
            return SERVICES[self.service]["module"].omit(self)
        return False
