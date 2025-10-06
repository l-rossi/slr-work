import csv

import pandas as pd

from typing import List
from typing import Dict


def sanitize(value):
    """Sanitize values for BibTeX format."""
    if not value:
        return ""
    return value.replace('{', '').replace('}', '').replace('\n', ' ').replace("℡", "TEL").strip()


def get_page_range(row):
    try:
        start = int(row["Start Page"])
        end = int(row["End Page"])
        return end - start + 1 if end >= start else 0
    except:
        return 0


def is_book(row, document_title):
    pub_title = row["Publication Title"].strip().lower()
    doc_title = row[document_title].strip().lower()
    same_title = doc_title == pub_title
    long_doc = get_page_range(row) >= 30
    no_vol_issue_meeting = not row["Volume"].strip() and not row["Issue"].strip() and not row.get("Meeting Date",
                                                                                                  "").strip()
    return ("book" in pub_title or "handbook" in pub_title) and same_title and no_vol_issue_meeting and long_doc


def is_inbook(row, document_title):
    pub_title = row["Publication Title"].strip().lower()
    doc_title = row[document_title].strip().lower()
    different_title = doc_title != pub_title
    short_doc = 0 < get_page_range(row) < 30
    return ("book" in pub_title or "handbook" in pub_title) and different_title and short_doc


def determine_entry_type(row, document_title):
    if is_book(row, document_title):
        return "book"
    elif is_inbook(row, document_title):
        return "inbook"

    pub_title = row["Publication Title"].lower()
    is_conference = bool(row.get("Meeting Date", "").strip()) or "conference" in pub_title

    if is_conference:
        return "inproceedings"
    elif pub_title:
        return "article"
    else:
        return "online"


def read_csv(file_name) -> List[Dict]:
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        data = [row for row in csv.DictReader(csvfile)]
    return data


def read_excel(file_name):
    df = pd.read_excel(file_name, dtype="str").fillna("")
    return df.to_dict('records')


def pages(row):
    if "Pages" in row:
        return sanitize(row["Pages"])

    if "Start Date" in row and "End Date" in row and row["Start Date"] and row["End Date"]:
        return f"{sanitize(row['Start Page'])}--{sanitize(row['End Page'])}"

    return ""


def normalize_research_rabbit_authors(authors):
    return " and ".join(authors.split("; ")[::2])


def fix_author_semi_colon(authors):
    return " and ".join(authors.split("; "))


def to_bibtex(input_csv, output_bib, offset=0, read_fn=read_csv, document_title="Document Title", author="Authors",
              url="PDF Link", map_authors=lambda x: x):

    print("reading", input_csv)
    reader = read_fn(input_csv)

    # Manually determined duplicates
    duplicates = {
        "PS_1196", "PS_1942", "PS_1948", "PS_1987", "PS_1997", "PS_2006", "PS_2026", "PS_2027", "PS_0609", "PS_0614",
        "PS_0917", "PS_0939", "PS_0950", "PS_0994", "PS_1207", "PS_1468", "PS_1474", "PS_1481", "PS_1575", "PS_1624",
        "PS_1666", "PS_1723", "PS_1811", "PS_1971", "PS_0903", "PS_0607", "PS_0610", "PS_0611", "PS_0612", "PS_0613",
        "PS_2406", "PS_0619", "PS_0620"
    }

    with open(output_bib, 'w', encoding='utf-8') as bibfile:
        for idx, row in enumerate(reader, offset + 1):
            entry_id = f"PS_{idx:04d}"

            if entry_id in duplicates:
                continue

            entry_type = determine_entry_type(row, document_title)
            bibfile.write(f"\n@{entry_type}{{{entry_id},\n")

            fields = {
                "author": sanitize(map_authors(row[author])),
                "title": f"{{{sanitize(row[document_title])}}}",
                "year": sanitize(row["Publication Year"]),
                "publisher": sanitize(row["Publisher"]),
                "doi": sanitize(row["DOI"]),
                "pages": pages(row),
                "volume": sanitize(row["Volume"]),
                "number": sanitize(row["Issue"]),
                "isbn": sanitize(row.get("ISBN", "") or row.get("ISBNs", "")),
                "issn": sanitize(row.get("ISSN", "")),
                "url": sanitize(row[url] if not row[url].startswith("https://scholar.google.com/") else "")
            }

            if entry_type == "article":
                fields["journal"] = sanitize(row["Publication Title"])
            elif entry_type == "inproceedings":
                fields["booktitle"] = sanitize(row["Publication Title"])
            elif entry_type in ["book", "inbook"]:
                fields["booktitle"] = sanitize(row["Publication Title"])

            for key, value in fields.items():
                if value:
                    bibfile.write(f"  {key} = {{{value}}},\n")

            bibfile.write("}\n")

if __name__ == "__main__":
    # IEEE exports second attempt
    input_csv_path = "./data/ieee_recovery/deduplicated.csv"
    output_bib_path = "./data/citation_data/ieee_dedpulicated.bib"
    to_bibtex(input_csv_path, output_bib_path, offset=584, map_authors=fix_author_semi_colon)

    input_csv_path = "./data/snowball_1.xlsx"
    output_bib_path = "./data/citation_data/snowball_1.bib"
    to_bibtex(input_csv_path, output_bib_path, offset=902, read_fn=read_excel, document_title="Title", author="Author",
              url="Link Attachments", map_authors=normalize_research_rabbit_authors)

    input_csv_path = "./data/snowball_ieee_recovery_extras.xlsx"
    output_bib_path = "./data/citation_data/snowball_ieee_extras.bib"
    to_bibtex(input_csv_path, output_bib_path, offset=2031, read_fn=read_excel, document_title="Title", author="Author",
              url="Link Attachments", map_authors=normalize_research_rabbit_authors)
    #
    input_csv_path = "./data/sd.xlsx"
    output_bib_path = "./data/citation_data/sd.bib"
    to_bibtex(input_csv_path, output_bib_path, offset=2079, read_fn=read_excel, document_title="Title", author="Author",
              url="Url", map_authors=fix_author_semi_colon)

    # IEEE first attempt
    input_csv_path = "./data/ieee.xlsx"
    output_bib_path = "./data/citation_data/ieee_first_iter.bib"
    to_bibtex(input_csv_path, output_bib_path, read_fn=read_excel, offset=2267, document_title="Title", author="Author",
              url="Url", map_authors=fix_author_semi_colon)
