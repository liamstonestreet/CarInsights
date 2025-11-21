import matplotlib.pyplot as plt
import os

def performance_vs_price_bubbles(df):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    metrics = [
        ("horsepower", "Horsepower"),
        ("performance", "0–100 km/h (sec)"),
        ("total_speed", "Top Speed (km/h)")
    ]

    colors = {
        "Petrol": "blue",
        "Diesel": "green",
        "Hybrid": "orange",
        "Electric": "red",
        "Unknown": "gray"
    }

    for ax, (col, label) in zip(axes, metrics):
        plot_df = df.dropna(subset=["price", col, "seats", "fuel_type"])
        scatter = ax.scatter(
            plot_df["price"], plot_df[col],
            s=plot_df["seats"] * 20,
            c=plot_df["fuel_type"].map(colors),
            alpha=0.6, edgecolors="w", linewidth=0.5
        )
        ax.set_xlabel("Price (USD)")
        ax.set_ylabel(label)
        ax.set_title(f"Price vs. {label}")

    plt.tight_layout()

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Save the figure
    output_path = os.path.join("output", "performance_vs_price.png")
    plt.savefig(output_path, dpi=300)
    print(f"Visualization saved to {output_path}")
