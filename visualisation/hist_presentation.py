import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df = pd.read_excel(
        "./data/search_union.xlsx"
    )

    # Keep only accepted papers
    df = df[df["Second Round Decision"].str.lower().str.startswith("yes")]

    # Extract year as integer series
    df["Year"] = df["Year"].astype(int)
    df["Topic"] = df["Demonstrated in Domain (This does not preclude genearl applicability)"].map(lambda x: "Healthcare" if "healthcare" in x.lower() else "Other")

    print(df["Demonstrated in Domain (This does not preclude genearl applicability)"])

    sns.set_theme(style="whitegrid")

    #     base_colors = ["#3EA5FF", "#00294A", "#BFE1FF", "#7FC3FF"]
    ax = sns.histplot(df, x="Year", multiple="stack", hue="Topic", binwidth=2, palette={
        "Healthcare": "#3EA5FF",
        "Other": "#00294A"
    })

    # Labels and title
    plt.xlabel("Year")
    plt.ylabel("# Papers")
    plt.title("Number of papers by publication date (2-year bins)")

    # Improve x tick labels to be integers
    xlabels = [str(int(x)) for x in ax.get_xticks() if pd.notna(x)]
    ax.set_xticklabels(xlabels)

    # Save to file (consistent with domain_hist saving convention)
    plt.tight_layout()
    plt.savefig("visualisation\\hist_presentation_healthcare.png", dpi=300)

