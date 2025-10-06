import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid Tkinter dependency
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

if __name__ == "__main__":
    data = [
        [1, 0.857142857, 1],
        [1, 0.75, 1],
        [1, 0.8, 1],
        [1, 1, 1],
        [0.75 * 0.5, 0.25 * 0.5, 1 * 0.5]
    ]

    df_data = []
    for i, triplet in enumerate(data):
        for j, value in enumerate(triplet):
            df_data.append({
                'Element': f'GS{i + 1}',
                'Bar': f'Q{j + 2}',
                'Value': value
            })

    df = pd.DataFrame(df_data)
    df["Element"] = df["Element"].astype("category")

    element_order = [f'GS{i+1}' for i in range(len(data))]
    plt.figure(figsize=(10, 6))
    hatches = ['', '///', '...']

    ax = sns.barplot(data=df, x='Element', y='Value', hue='Bar', palette='viridis', order=element_order)

    # Add hatching patterns to make bars distinct in B&W
    bars = ax.patches

    for i, bar in enumerate(bars):
        hatch_index = i // 5 if i < 15 else i % 3
        bar.set_hatch(hatches[hatch_index])
        bar.set_edgecolor('gray')

    # ✅ Remove tick marks; keep default categorical labels centered under groups
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    plt.title('Success by Entry in the Gold Standard', fontsize=16, fontweight='bold')
    plt.xlabel('Regulation Fragments', fontsize=12)
    plt.ylabel('Success Score', fontsize=12)
    plt.ylim(0, 1)

    plt.grid(axis='y', alpha=0.3)
    plt.legend(title='Evaluation Criteria', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    output_path = "E:/MastersThesis/SLR/slr-work/visualisation/eval_use_case.png"
    plt.savefig(output_path, dpi=600)
    # plt.show()
