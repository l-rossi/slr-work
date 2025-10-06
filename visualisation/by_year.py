import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


if __name__ == "__main__":
    df = pd.read_excel("./data/search_union.xlsx")
    df = df[df["Second Round Decision"].eq("Yes")]

    data = df["Year"].astype(int)

    # Set visual theme
    sns.set_theme(style="darkgrid")

    # Plot histogram with one bin per integer (set bin edges manually)
    sns.histplot(data, binwidth=1)

    # Labels and title
    plt.xlabel("Year")
    plt.ylabel("# Papers")
    plt.title("Number of papers per year") # TODO this is not per year, but per bucket size years...

    plt.show()
