import pandas as pd
from scipy.stats.contingency import association
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

# Provide DataFrame with categorical columns
if __name__ == "__main__":
    df = pd.read_excel("./data/search_union.xlsx")
    df = df[df["Second Round Decision"].eq("Yes")]

    # print(tuples)

    matrix = pd.crosstab(df["Automation Normalized"], df["BPC Normalized"])
    print(matrix)
    #
    print("cramer", association(matrix, method="cramer"))
    print("tschuprow", association(matrix, method="tschuprow"))

    df["Year"] = df["Year"].astype(int)
    print(df.dtypes)

    sns.set_theme(style="whitegrid", palette="Set2")
    # plt.ticklabel_format(style="sci")
    ax = sns.histplot(
        data=df,
        x='Year',
        hue='Automation Normalized',
        binwidth=3,
        multiple='fill',
        hue_order=reversed(['Automated', 'Semi-Automated', 'Tool Assisted', 'Manual'])
    )
    # ax.legend(framealpha=1)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x)}'))

    # print(ax.get_xticks())
    # xlabels = [str(int(x)) for x in ax.get_xticks()]
    # print(xlabels)
    # ax.set_xticklabels(xlabels)

    plt.ylabel('Proportion')
    plt.title('Level of automation over time')
    plt.show()

    exit()

    sns.set_theme(style="whitegrid", palette="Set2")

    data = pd.DataFrame({
        "Year": df["Year"].astype(int),
        "Topic": df["Automation Normalized"],
    })
    count = df["Automation Normalized"].value_counts()
    # ax = sns.histplot(data, binwidth=2, multiple="stack", x='Year', hue='Topic', legend=True)
    print(count)
    print(count.keys())
    patches, texts = plt.pie(df["Automation Normalized"].value_counts())
    labels = [
        f"Manual ({count['Manual']})",
        f"Semi-Automated ({count['Semi-Automated']})",
        f"Automated ({count['Automated']})",
        f"Tool-Assisted ({count['Tool Assisted']})",
    ]
    plt.legend(patches, labels, loc="best", frameon=False)
    plt.axis('equal')
    plt.tight_layout()

    # Labels and title
    # plt.xlabel("Year")
    # plt.ylabel("# Papers")
    # plt.title("Number of papers by publication date")  # TODO this is not per year, but per bucket size years...

    # plt.grid()

    # legend = ax.legend()
    # legend.get_frame().set_facecolor('lightgray')

    # plt.show()
    plt.savefig("ugly_automation_pie.png", dpi=300)
