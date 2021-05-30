class UsageRecord(object):
    def __init__(self, data):
        self._data = data

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
