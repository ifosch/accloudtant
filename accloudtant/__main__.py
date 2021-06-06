from accloudtant import load_data


if __name__ == "__main__":
    usage = load_data("tests/fixtures/2021/03/S3.csv")

    print("Simple Storage Service")
    for area, concepts in usage.totals(omit=lambda x: x.is_data_transfer or x.type == "StorageObjectCount"):
        print("\t", area)
        for c, v, u in concepts:
            print("\t\t{}\t{} {}".format(c, v, u))

    data_transfers = usage.data_transfers()
    if len(data_transfers) > 0:
        print("Data Transfer")
        for area, concepts in data_transfers.totals(omit=lambda x: not x.is_data_transfer):
            print("\t", area)
            for c, v, u in concepts:
                print("\t\t{}\t{} {}".format(c, v, u))
