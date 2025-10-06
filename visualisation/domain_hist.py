import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df = pd.read_excel(
        "./data/search_union.xlsx"
    )

    df = df[df["Second Round Decision"].str.lower().str.startswith("yes")]


    def categorize(x: str) -> str:
        l = x.lower()

        if "general" in l:
            return "No focus on singular domain"

        if "privacy" in l:
            return "Privacy"
        #
        # if "finance" in l:
        #     return "Finance"
        #
        # if "tax" in l:
        #     return "Taxation"
        #
        # if "trade" in l:
        #     return "Trade Secrets"

        # if "criminal" in l:
        #     return "Criminal Law"

        return "Other"


    data = pd.DataFrame({
        "Year": df["Year"].astype(int),
        "Topic": df["Demonstrated in Domain (This does not preclude genearl applicability)"].map(categorize),
    })

    sns.set_theme(style="whitegrid", palette="Set2")

    # Plot histogram with one bin per integer (set bin edges manually)
    ax = sns.histplot(data, binwidth=2, multiple="stack", x='Year', hue='Topic', legend=True,
                      hue_order=['No focus on singular domain', 'Other', 'Privacy', ])

    # Labels and title
    plt.xlabel("Year")
    plt.ylabel("# Papers")
    plt.title("Number of papers by publication date")  # TODO this is not per year, but per bucket size years...

    plt.grid()

    xlabels = [str(int(x)) for x in ax.get_xticks()]
    ax.set_xticklabels(xlabels)

    # legend = ax.legend()
    # legend.get_frame().set_facecolor('lightgray')

    # plt.show()
    plt.savefig("domain_hist.png", dpi=300)
    print(data)
