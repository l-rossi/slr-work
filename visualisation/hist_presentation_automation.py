import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Load the same dataset and apply the same preprocessing as other hist scripts
    df = pd.read_excel("./data/search_union.xlsx")
    df = df[df["Second Round Decision"].str.lower().str.startswith("yes")]

    # Ensure Year is integer
    df["Year"] = df["Year"].astype(int)

    # Use the automation metric also used in creation_automation.py
    # Column is "Automation Normalized" with categories such as
    # ['Automated', 'Semi-Automated', 'Tool Assisted', 'Manual']
    metric_col = "Automation Normalized"

    # Drop rows where metric is missing
    df = df[df[metric_col].notna()]

    # Presentation color scheme (as used in presentation scripts)
    # Base palette from presentation_automatation.py
    base_colors = [
        "#BFE1FF",
        "#7FC3FF",
        "#3EA5FF",
        "#00294A",
    ]

    # Map consistent colors to expected categories; fall back cycling if others appear
    categories = ["Automated", "Semi-Automated", "Tool Assisted", "Manual"]
    color_map = {cat: base_colors[i % len(base_colors)] for i, cat in enumerate(categories)}

    # Build hue order to keep legend and stacking consistent
    # Use the same semantic grouping but for stacked histogram we want counts per bin
    hue_order = [c for c in categories if c in set(df[metric_col])]

    sns.set_theme(style="whitegrid")

    # Create a stacked histogram over time for the automation metric
    ax = sns.histplot(
        data=df,
        x="Year",
        hue=metric_col,
        multiple="stack",
        binwidth=2,
        palette=color_map,
        hue_order=hue_order,
        legend=True,
    )

    # Labels and title
    plt.xlabel("Year")
    plt.ylabel("# Papers")
    plt.title("Number of papers by publication date (2-year bins) — Automation levels")

    # Improve integer x tick labels like other scripts
    xlabels = [str(int(x)) for x in ax.get_xticks() if pd.notna(x)]
    ax.set_xticklabels(xlabels)

    plt.tight_layout()
    # Save with naming aligned to other presentation outputs
    plt.savefig("visualisation\\hist_presentation_automation.png", dpi=300)
