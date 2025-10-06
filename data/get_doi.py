import csv

files = ["ieee.csv", "acm.csv", "sd.csv"]

dois = dict()

for file in files:
    with open(file, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        header = next(reader)
        index = header.index("DOI")

        for line in reader:
            doi = line[index].removeprefix("https://").strip()
            if doi:
                dois[doi] = (file,)

while True:
    inp = input()
    if inp == "q":
        break

    doi = inp.removeprefix("https://").strip()
    print(dois.get(doi))
