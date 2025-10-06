import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == "__main__":
    # Load data and filter to selected studies
    df = pd.read_excel("./data/search_union.xlsx")
    df = df[df["Second Round Decision"].eq("Yes")]

    # Count occurrences of each Level of Automation
    involvement = df["Automation Normalized"].value_counts()

    # Prepare labels and sizes for the pie chart
    labels = involvement.index.tolist()
    sizes = involvement.values.tolist()

    # Define required colors (cycle if there are more than 4 categories)
    base_colors = ["#3EA5FF", "#00294A", "#BFE1FF", "#7FC3FF"]
    colors = [base_colors[i % len(base_colors)] for i in range(len(labels))]

    # Reassign colors per request:
    # - Manual should take the color currently assigned to Semi-Automated
    # - Automated and Tool Assisted should swap their colors
    try:
        idx_manual = labels.index("Manual") if "Manual" in labels else None
        idx_semi = labels.index("Semi-Automated") if "Semi-Automated" in labels else None
        if idx_manual is not None and idx_semi is not None and idx_manual != idx_semi:
            colors[idx_manual], colors[idx_semi] = colors[idx_semi], colors[idx_manual]
    except Exception:
        pass
    try:
        idx_auto = labels.index("Automated") if "Automated" in labels else None
        idx_tool = labels.index("Tool Assisted") if "Tool Assisted" in labels else None
        if idx_auto is not None and idx_tool is not None and idx_auto != idx_tool:
            colors[idx_auto], colors[idx_tool] = colors[idx_tool], colors[idx_auto]
    except Exception:
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
    legend = plt.legend(wedges, labels, title="Level of Automation", loc="center left", bbox_to_anchor=(1, 0.5))
    # Ensure legend text is readable regardless of swatch color
    for text in legend.get_texts():
        text.set_color("#111111")
    if legend.get_title() is not None:
        legend.get_title().set_color("#111111")

    # Optional title
    plt.title("Level of Automation")

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
    plt.savefig("presentation_automation.png", dpi=300, bbox_inches="tight")