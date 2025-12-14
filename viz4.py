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

# from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from wordcloud import WordCloud, STOPWORDS
import spacy
import pandas as pd
from preprocess import preprocess_recall_data

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

# ---------- Viz 4: Recall wordcloud ----------

# uses datasource 4 (recall data)
def viz4(df):
    """
    Visualization 4: Wordcloud of recall SUMMARY text.

    Takes the preprocessed recall dataframe (with SUMMARY column),
    builds a wordcloud, and saves it to output/recall_wordcloud.png.
    """

    # Combine all summaries into one big string
    summaries = df["SUMMARY"].dropna().astype(str)
    if summaries.empty:
        print("No SUMMARY text available for wordcloud.")
        return

    full_text = " ".join(summaries.tolist())

    # Base stopwords + some recall-specific ones to avoid boring words
    stopwords = set(STOPWORDS)
    extra_stops = {
        "recall", "vehicle", "vehicles", "honda", "acura", "toyota", "ford",
        "customer", "service", "team", "contacting", "urgent", "safety",
        "please", "may", "could", "cause", "affected", "owners", "owner",
        "dealers", "dealer", "free", "charge", "repair", "repairs",
        # "notice", "followup", "follow", "bulletin", "information", "additional",
        # "part", "parts", "system", "systems", "may", "will", "also", "one",
        # "two", "use", "used", "using", "within", "without", "including",
        # "ensure", "ensure", "check", "checks", "checking"
    }
    stopwords |= extra_stops

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
    #output_path = os.path.join("output", "recall_wordcloud.svg")
    plt.tight_layout(pad=0)
    # plt.savefig(output_path, dpi=300)
    plt.savefig(output_path, dpi=600, format="png")
    plt.close()

    print(f"Visualization 4 (wordcloud) saved to {output_path}")

if __name__ == "__main__":
    # For testing purposes only
    

    recall_path = "data/recall"
    recall_df = preprocess_recall_data(recall_path)
    viz4(recall_df)