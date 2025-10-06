import csv
from collections import defaultdict


def clean_doi(doi: str) -> str:
    return  doi.removeprefix("https://doi.org/").strip()

if __name__ == "__main__":

    existing_paper_files = ["ieee.csv", "acm.csv", "sd.csv", "ResearchRabbit_Export_26.3.2025.csv", "ieee_recovery/ieee_second_attempt.csv"]
    new_paper_file = "ieee_recovery/snowball_2_raw.csv"

    existing_dois = dict()

    for file in existing_paper_files:
        with open(file, encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=",")
            header = next(reader)
            # index = header.index("DOI")
            index = next(i for i, x in enumerate(header) if x == "Title" or x == "Document Title")

            for line in reader:
                doi = clean_doi(line[index])
                if doi:
                    existing_dois[doi] = (file,)

    new_papers = defaultdict(list)
    with open(new_paper_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        header = next(reader)
        # index = header.index("DOI")
        index = header.index("Title")
        for i, line in enumerate(reader):
            doi = clean_doi(line[index])
            # print(doi)
            if not doi or doi not in existing_dois:
                new_papers[doi].append(line)

    # with open("ieee_recovery/snowball_2_deduplicated.csv", "w+", encoding="utf-8", newline='') as f:
    #     writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
    #     writer.writerow(header)
    #     for paper_group in new_papers.values():
    #         writer.writerows(paper_group)

    print(sum(len(x) for x in new_papers.values()))

    print(len(new_papers))
