import matplotlib.pyplot as plt
import os
import mplcursors


from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QComboBox,
    QLabel,      
)


from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from wordcloud import WordCloud, STOPWORDS
import spacy

# Make sure you've run:
#   pip install spacy
#   python -m spacy download en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
    # increase the size of the wordcloud
    # nlp.max_length = 70538817
except OSError as e:
    raise OSError(
        "spaCy model 'en_core_web_sm' not found. "
        "Install it with: python -m spacy download en_core_web_sm"
    ) from e

def performance_vs_price_bubbles(df):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    metrics = [
        ("horsepower", "Horsepower"),
        ("performance", "0–100 km/h (sec)"),
        ("total_speed", "Top Speed (km/h)"),
    ]

    colors = {
        "Petrol": "blue",
        "Diesel": "green",
        "Hybrid": "orange",
        "Electric": "red",
        "Unknown": "gray",
    }

    for ax, (col, label) in zip(axes, metrics):
        plot_df = df.dropna(subset=["price", col, "seats", "fuel_type"])
        ax.scatter(
            plot_df["price"],
            plot_df[col],
            s=plot_df["seats"] * 20,
            c=plot_df["fuel_type"].map(colors),
            alpha=0.6,
            edgecolors="w",
            linewidth=0.5,
        )
        ax.set_xlabel("Price (USD)")
        ax.set_ylabel(label)
        ax.set_title(f"Price vs. {label}")

    plt.tight_layout()

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", "performance_vs_price.png")
    plt.savefig(output_path, dpi=300)
    print(f"Visualization saved to {output_path}")


# ---------- Viz 3 placeholder (wordcloud will go here later) ----------

# uses datasource 4 (recall data)
def viz3(df):
    """
    Visualization 3: Wordcloud of recall SUMMARY text.

    Takes the preprocessed recall dataframe (with SUMMARY column),
    builds a wordcloud, and saves it to output/recall_wordcloud.png.
    """

    # Combine all summaries into one big string
    summaries = df["SUMMARY"].dropna().astype(str)
    if summaries.empty:
        print("No SUMMARY text available for wordcloud.")
        return

    full_text = " ".join(summaries.tolist()).lower()

    # Base stopwords + some recall-specific ones to avoid boring words
    stopwords = set(STOPWORDS)
    extra_stops = {
        "recall", "vehicle", "vehicles", "honda", "acura", "toyota", "ford",
        "customer", "service", "team", "contacting", "urgent", "safety",
        "please", "may", "could", "cause", "affected", "owners", "owner",
        "dealers", "dealer", "free", "charge", "repair", "repairs",
        "notice", "followup", "follow", "bulletin", "Impreza", "Civic",
        "Accord", "CRV", "Pilot", "Camry", "Corolla", "RAV4", "F150", "occupant",
        "Dodge", "Chrysler", "Jeep", "Ram", "letter", "appointment", "Letter",
        "Takata", "AMENDMENT", "previous", "event", "regarding", "equipped",
        "model year", "gregory", "gunther", "year", "2x", "Due", "potentially",
        "revised"
    }
    stopwords |= {w.lower() for w in extra_stops} # or operator (union)

    # Generate wordcloud
    wc = WordCloud(
        width=1600,
        height=800,
        background_color="white",
        stopwords=stopwords,
        collocations=True  # keep common two-word phrases
    ).generate(full_text)

    # Plot and save
    plt.figure(figsize=(14, 7))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Common Terms in Recall Summaries")

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", "recall_wordcloud.png")
    plt.tight_layout(pad=0)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Visualization 3 (wordcloud) saved to {output_path}")

def viz3_2(df):
    """
    Visualization 3: Wordcloud of recall SUMMARY text, with spaCy noun phrases.

    - Uses raw SUMMARY text.
    - Extracts multi-word noun phrases with spaCy (e.g. "front passenger airbag").
    - Adds those phrases (underscored) back into the text so WordCloud
      treats them as single tokens.
    """

    summaries = df["SUMMARY"].dropna().astype(str)
    if summaries.empty:
        print("No SUMMARY text available for wordcloud.")
        return

    full_text = " ".join(summaries.tolist())

    # Base stopwords + some recall-specific ones
    stopwords = set(STOPWORDS)
    extra_stops = {
        "recall", "vehicle", "vehicles", "honda", "acura", "toyota", "ford",
        "customer", "service", "team", "contacting", "urgent", "safety",
        "please", "may", "could", "cause", "affected", "owners", "owner",
        "dealers", "dealer", "free", "charge", "repair", "repairs",
        "notice", "followup", "follow", "bulletin", "Impreza", "Civic",
        "Accord", "CRV", "Pilot", "Camry", "Corolla", "RAV4", "F150", "occupant",
        "Dodge", "Chrysler", "Jeep", "Ram", "letter mailed", "appointment", "Letter",
        "Takata", "AMENDMENT", "previous version", "event", "regarding",
    }
    stopwords |= {w.lower() for w in extra_stops}

    # ---------- spaCy noun-phrase extraction ----------
    doc = nlp(full_text)

    phrase_tokens = []
    for chunk in doc.noun_chunks:
        # Drop punctuation tokens
        tokens = [t.text.lower() for t in chunk if not t.is_punct]

        # Need at least 2 words for a "phrase"
        if len(tokens) < 2:
            continue

        # Skip phrases that are all stopwords
        if all(tok in stopwords for tok in tokens):
            continue

        # Underscore-join so WordCloud treats phrase as one token
        phrase = "_".join(tokens)
        phrase_tokens.append(phrase)

    # Combine original text with noun-phrase tokens
    combined_text = full_text + " " + " ".join(phrase_tokens)

    # ---------- Generate wordcloud ----------
    wc = WordCloud(
        width=1600,
        height=800,
        background_color="white",
        stopwords=stopwords,
        collocations=False,  # we provide our own phrases
    ).generate(combined_text)

    plt.figure(figsize=(14, 7))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Common Terms and Phrases in Recall Summaries")

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", "recall_wordcloud_2.png")
    plt.tight_layout(pad=0)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Visualization 3 (wordcloud) saved to {output_path}")


# ---------- Viz 4: Interactive recall trends by MODEL YEAR + MAKE ----------

class RecallTrendsWindow(QMainWindow):
    def __init__(self, df, default_make: str = "SUBARU"):
        super().__init__()
        self.df = df

        self.setWindowTitle("Recall Trends by Model Year and Make")

        # central widget / layout
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # --------- MAKE dropdown + label ---------
        make_label = QLabel("Make:")
        layout.addWidget(make_label)

        self.make_combo = QComboBox()
        makes = sorted(self.df["MAKE"].dropna().unique())
        self.make_combo.addItems(makes)

        # default brand = SUBARU if present
        if default_make in makes:
            idx = makes.index(default_make)
            self.make_combo.setCurrentIndex(idx)

        layout.addWidget(self.make_combo)

        # --------- MODEL dropdown + label ---------
        model_label = QLabel("Model:")
        layout.addWidget(model_label)

        self.model_combo = QComboBox()
        layout.addWidget(self.model_combo)

        # matplotlib figure + canvas
        self.fig = Figure(figsize=(12, 6))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # make dropdowns stick to the top
        layout.setStretch(layout.indexOf(make_label), 0)
        layout.setStretch(layout.indexOf(self.make_combo), 0)
        layout.setStretch(layout.indexOf(model_label), 0)
        layout.setStretch(layout.indexOf(self.model_combo), 0)
        layout.setStretch(layout.indexOf(self.canvas), 1)

        # wire up signals
        self.make_combo.currentTextChanged.connect(self.on_make_changed)
        self.model_combo.currentTextChanged.connect(self.update_plot)

        # initial population of model list + plot
        self.on_make_changed()

    # ---------- when MAKE changes, repopulate MODEL list ----------
    def on_make_changed(self):
        make = self.make_combo.currentText()
        df_brand = self.df[self.df["MAKE"] == make]

        self.model_combo.blockSignals(True)
        self.model_combo.clear()

        if df_brand.empty:
            # no models; still try to update plot
            self.model_combo.addItem("All models")
        else:
            models = sorted(df_brand["MODEL"].dropna().unique())
            self.model_combo.addItem("All models")
            self.model_combo.addItems(models)

        self.model_combo.setCurrentIndex(0)
        self.model_combo.blockSignals(False)

        # update plot for new make + default "All models"
        self.update_plot()

    # ---------- main plotting logic ----------
    def update_plot(self):
        make = self.make_combo.currentText()
        model = self.model_combo.currentText()

        # Clear figure
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        # Filter by MAKE (and MODEL if specified)
        df_brand = self.df[self.df["MAKE"] == make]

        if model != "All models":
            df_brand = df_brand[df_brand["MODEL"] == model]

        if df_brand.empty:
            ax.set_title(f"No data for {make} ({model})")
            self.canvas.draw()
            return

        # Count distinct recalls per year
        grouped = df_brand.groupby("MODEL YEAR")["NHTSA ID"].nunique()

        # Build full continuous year range
        min_year = int(df_brand["MODEL YEAR"].min())
        max_year = int(df_brand["MODEL YEAR"].max())
        all_years = list(range(min_year, max_year + 1))

        grouped_full = grouped.reindex(all_years, fill_value=0)

        years = grouped_full.index.to_list()
        counts = grouped_full.values

        # Plot (w/ tooltip!)
        # ax.plot(years, counts, marker="o")
        # ax.set_xlabel("Model Year")
        # ax.set_ylabel("Number of distinct recalls")

        # Plot
        line, = ax.plot(years, counts, marker="o")
        ax.set_xlabel("Model Year")
        ax.set_ylabel("Number of distinct recalls")

        # -------- Hover tooltips with mplcursors --------
        # keep a reference on self so it doesn't get garbage-collected
        self.cursor = mplcursors.cursor(line, hover=True)

        @self.cursor.connect("add")
        def on_add(sel, years=years, counts=counts):
            i = sel.index
            year = years[i]
            count = counts[i]
            sel.annotation.set(
                text=f"Year: {year}\nRecalls: {count}",
                fontsize=9,
            )


        title_suffix = "" if model == "All models" else f" – {model}"
        ax.set_title(f"Recall Trends for {make}{title_suffix} (by Model Year)")
        ax.grid(True)

        # ------------ Custom Year Formatter (your version) ------------
        def format_year(year: int) -> str:
            """Return `'YY` for 1900s, `YY` for 2000+."""
            first_two = year // 100
            yy = year % 100
            if first_two == 19:
                return f"'{yy:02d}"
            return f"{yy:02d}"

        # X-axis ticks (one per year)
        ax.set_xticks(years)
        ax.set_xticklabels([format_year(y) for y in years], rotation=45)

        # Y-axis integer-only ticks
        max_y = grouped_full.max()
        ax.set_yticks(range(0, max(max_y + 1, 5)))

        self.fig.tight_layout()
        self.canvas.draw()


def viz4(df):
    """
    Entry point for Visualization 4.

    Returns a RecallTrendsWindow that main.py can show.
    """
    return RecallTrendsWindow(df, default_make="SUBARU")
