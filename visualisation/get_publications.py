import re
from typing import List

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":

    sources = [
        "acm.xlsx",
        "ieee.xlsx",
        "ieee_second_export.xlsx",
        "sd.xlsx",
        "snowball_1.xlsx",
        "snowball_ieee_recovery_extras.xlsx",
    ]

    ident_to_pub = dict()

    for s in sources:
        df = pd.read_excel(f"./data/{s}").fillna("")

        print("reading", s)
        print(len(ident_to_pub))
        ident_to_pub.update(
            dict(zip(df["Identifier"], df["Publication Title"]))
        )
        print(len(ident_to_pub))

        # print(df["Identifier"], df["Publication Title"])

    relevant_rows = pd.read_excel("./data/search_union.xlsx")
    relevant_rows = relevant_rows[relevant_rows["Second Round Decision"].str.lower().str.startswith("yes")]

    assert len(relevant_rows) == 240

    # print(len(relevant_idents))

    print(len(ident_to_pub))

    ls: List[str] = relevant_rows["Identifier"].map(ident_to_pub).tolist()

    # print(ls)

    s = {
        re.sub(r"^(?:Companion )?Proceedings\.? of the \w+ |^\d{4} \w+ |\d\w{2} ", "", x) for x in ls if x
    }

    data = pd.DataFrame({
        "year": relevant_rows["Year"].astype(int),
        "pub": relevant_rows["Publication Title"].fillna("Other").map(
            lambda x: re.sub(r"^(?:Companion )?Proceedings\.? of the \w+ |^\d{4} \w+ |\d\w{2} ", "", x))
    })

    print(set(data["pub"]))

    print(len(set(data["pub"]))) # 97 categories...

    sns.set_theme(style="darkgrid")

    # Plot histogram with one bin per integer (set bin edges manually)
    sns.histplot(data, binwidth=1, multiple="stack", x='year', hue='pub', legend=False)

    # Labels and title
    plt.xlabel("Year")
    plt.ylabel("# Papers")
    plt.title("Number of papers per year")  # TODO this is not per year, but per bucket size years...

    top_pubs = data['pub'].value_counts().nlargest(10)
    print(top_pubs)
    # sns.countplot(
    #     data=data[data["pub"].isin(top_pubs)],
    #     order=top_pubs.index,
    #     x="pub"
    # )

    plt.show()
