import csv


if __name__ == "__main__":
    usage = []

    with open("tests/fixtures/2021/03/S3.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            usage.append(row)

    print("Simple Storage Service")
    for entry in usage:
        print(entry)
