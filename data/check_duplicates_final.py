import csv

from collections import Counter

def clean_doi(doi: str) -> str:
    return  doi.removeprefix("https://doi.org/").strip()

if __name__ == "__main__":

    c = Counter()

    with open("search_union.csv", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        # index = header.index("DOI")
        print(header)
        index = next(i for i, x in enumerate(header) if x == "Title" or x == "Document Title")

        for line in reader:
            doi = clean_doi(line[index])
            if doi:
                c[doi] += 1

    print([(x, c[x]) for x in c.elements() if c[x] > 1])