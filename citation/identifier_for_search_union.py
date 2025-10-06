import re

import pandas as pd


def read_bib(txt: str):
    entries = txt.split("\n\n")

    re_title = re.compile(r"title = {(.*)},")
    re_doi = re.compile(r"doi = {(.*)},")
    re_identifier = re.compile(r"@\w+{(PS_\d{4}),")

    for e in entries:
        print(e)
        title = re_title.search(e).group(1).replace("{", "").replace("}", "")
        doi = re_doi.search(e)
        identifier = re_identifier.search(e).group(1)

        yield (
            identifier,
            doi.group(1) if doi is not None else "",
            title,
        )


if __name__ == "__main__":
    bib_files = [
        "acm_normalized.bib", "sd.bib", "ieee_dedpulicated.bib", "snowball_1.bib", "snowball_ieee_extras.bib",
        "ieee_first_iter.bib"
    ]

    doi_title_to_identifier = dict()

    for f in bib_files:
        with open(f"./data/citation_data/{f}", encoding="utf-8") as input_file:
            data = input_file.read()

        for (identifier, doi, title) in read_bib(data):
            if (doi, title) in doi_title_to_identifier:
                raise Exception(f"Duplicates {identifier} and {doi_title_to_identifier[(doi, title)]}")

            doi_title_to_identifier[(doi, title)] = identifier

    # Expect 2422
    print(len(doi_title_to_identifier))

    identifier_list = []
    search_union = pd.read_excel("./data/search_union.xlsx").fillna("")

    # Might have to remove for pasting identifiers into excel
    search_union = search_union[search_union["Second Round Decision"].str.lower().str.startswith("yes")]

    for _, row in search_union.iterrows():
        identifier = doi_title_to_identifier[(row["DOI"], row["Title"])]
        identifier_list.append(identifier)

    print(len(identifier_list))
    print(identifier_list)
    print("\n".join([fr"\citefield{{{x}}}{{title}} & \citeauthor{{{x}}} & \cite{{{x}}}     \\" for x in identifier_list]))


