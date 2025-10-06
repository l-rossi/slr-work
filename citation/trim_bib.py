import re

import pandas as pd

if __name__ == "__main__":

    search_union = pd.read_excel(
        "./data/search_union.xlsx"
    )

    search_union = search_union[
        search_union["Second Round Decision"].eq("Yes")
    ]

    print(len(search_union))

    identifiers = set(search_union["Identifier"].tolist())

    bib_files = [
        "acm_normalized.bib", "sd.bib", "ieee_dedpulicated.bib", "snowball_1.bib", "snowball_ieee_extras.bib",
        "ieee_first_iter.bib"
    ]

    bibs = []
    for f in bib_files:
        with open(f"./data/citation_data/{f}", encoding="utf-8") as input_file:
            bibs.extend(input_file.read().split("\n\n"))

    re_identifier = re.compile(r"@\w+{(PS_\d{4}),")

    print(len(bibs))

    retained_bibs = [
        bib for bib in bibs if re_identifier.search(bib).group(1) in identifiers
    ]

    print(len(retained_bibs))

    with open("./data/citation_data/slr_primary_studies.bib", "w", encoding="utf-8") as f:
        f.write("\n\n".join(retained_bibs))
