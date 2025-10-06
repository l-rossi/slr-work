
import pandas as pd
from scipy.stats.contingency import association


# Provide DataFrame with categorical columns
if __name__ == "__main__":
    df = pd.read_excel("./data/search_union.xlsx")
    df = df[df["Second Round Decision"].eq("Yes")]


    # print(tuples)

    matrix = pd.crosstab(df["Incolvment Normalized"], df["BPC Normalized"])
    print(matrix)

    print("cramer", association(matrix, method="cramer"))
    print("tschuprow", association(matrix, method="tschuprow"))