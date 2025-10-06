import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib_venn import venn2

if __name__ == "__main__":
    df = pd.read_excel("data/search_union.xlsx")
    df = df[df["Second Round Decision"].eq("Yes")]

    mask_case = df["Case Focus (Common Law)"].str.lower().str.startswith("yes")
    mask_statute = df["Statutes focus (Civil Law)"].str.lower().str.startswith("yes")

    case = df[mask_case]
    statue = df[mask_statute]
    both = df[mask_statute & mask_case]
    print(len(df))
    print(len(case), len(statue), len(both))

    venn2(subsets=(len(case) - len(both), len(statue) - len(both), len(both)), set_labels=('Focus on Cases', 'Focus on Statutes'))

    # data = df["Year"].astype(int)
    #
    # # Set visual theme
    # sns.set_theme(style="darkgrid")
    #
    # # Plot histogram with one bin per integer (set bin edges manually)
    # sns.histplot(data, binwidth=1)
    #
    # # Labels and title
    # plt.xlabel("Year")
    # plt.ylabel("# Papers")
    # plt.title("Number of papers per year")
    #
    plt.show()
