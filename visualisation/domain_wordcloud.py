import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

if __name__ == "__main__":

    df = pd.read_excel(
        "./data/search_union.xlsx"
    )

    df = df[df["Second Round Decision"].str.lower().str.startswith("yes")]


    terms = df["Demonstrated in Domain (This does not preclude genearl applicability)"].tolist()
    terms = [x.strip().lower().replace("law", "") for x in terms if "General" not in x.strip() and x.strip() != "Law"]

    print(terms)



    # Combine terms into a single string
    text = ' '.join(terms)

    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()