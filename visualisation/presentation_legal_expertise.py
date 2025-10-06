import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == "__main__":
    # Load data and filter to selected studies
    df = pd.read_excel("./data/search_union.xlsx")
    df = df[df["Second Round Decision"].eq("Yes")]

    # Count occurrences of each Legal Expertise (column name kept as provided)
    involvement = df["Incolvment Normalized"].value_counts()

    # Prepare labels and sizes for the pie chart
    labels = involvement.index.tolist()
    sizes = involvement.values.tolist()

    # Define required colors (cycle if there are more than 4 categories)
    base_colors = ["#3EA5FF", "#00294A", "#BFE1FF", "#7FC3FF"]
    colors = [base_colors[i % len(base_colors)] for i in range(len(labels))]

    # If both categories 'No' and 'Author' exist, swap their assigned colors
    try:
        idx_no = labels.index("No") if "No" in labels else None
        idx_author = labels.index("Author") if "Author" in labels else None
        if idx_no is not None and idx_author is not None:
            colors[idx_no], colors[idx_author] = colors[idx_author], colors[idx_no]
    except Exception:
        # Silently ignore if anything unexpected happens; fall back to default colors
        pass

    # If both categories 'Acknowledgment' and 'Evaluation' exist, swap their assigned colors
    try:
        idx_ack = labels.index("Acknowledgment") if "Acknowledgment" in labels else None
        idx_eval = labels.index("Evaluation") if "Evaluation" in labels else None
        if idx_ack is not None and idx_eval is not None:
            colors[idx_ack], colors[idx_eval] = colors[idx_eval], colors[idx_ack]
    except Exception:
        # Silently ignore if anything unexpected happens; fall back to default colors
        pass


    # Create figure
    plt.figure(figsize=(6, 6))
    sns.set_style("whitegrid")

    # Create the pie chart
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=None,  # we'll use legend for labels for clarity
        colors=colors,
        autopct="%1.0f%%",
        startangle=90,
        counterclock=False,
        pctdistance=0.7,
    )

    # Improve slice separation
    for w in wedges:
        w.set_edgecolor("white")
        w.set_linewidth(1.0)

    # Ensure the pie is drawn as a circle
    plt.gca().axis('equal')

    # Add legend mapping wedges to labels
    legend = plt.legend(wedges, labels, title="Legal Expertise", loc="center left", bbox_to_anchor=(1, 0.5))
    # Ensure legend text is readable regardless of swatch color
    for text in legend.get_texts():
        text.set_color("#111111")
    if legend.get_title() is not None:
        legend.get_title().set_color("#111111")

    # Optional title
    plt.title("Legal Expertise")

    # Improve readability of autopct labels by choosing color based on slice luminance
    import matplotlib.colors as mcolors
    def ideal_text_color(hex_color: str) -> str:
        rgb = mcolors.to_rgb(hex_color)
        # Relative luminance (sRGB)
        l = 0.2126*rgb[0] + 0.7152*rgb[1] + 0.0722*rgb[2]
        return "black" if l > 0.6 else "white"
    # Map wedge facecolor to appropriate text color
    for w, at in zip(wedges, autotexts):
        fc = w.get_facecolor()  # RGBA
        hexc = mcolors.to_hex(fc)
        at.set_color(ideal_text_color(hexc))
        at.set_fontweight("bold")
        at.set_bbox(dict(facecolor="none", edgecolor="none", pad=0.2))

    plt.tight_layout()
    plt.savefig("presentation_legal_expertise.png", dpi=300, bbox_inches="tight")