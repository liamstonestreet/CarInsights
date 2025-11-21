import sys
import pandas as pd

from PyQt6.QtWidgets import QApplication

from preprocess import preprocess_cars2025, preprocess_recall_data
from visualize import performance_vs_price_bubbles, viz3, viz4


def main():
    # -------- Visualization 1: Performance vs Price (static, saved to file) --------
    # cars_path = "data/cars_2025.csv"
    # cars_df = pd.read_csv(cars_path, encoding="cp1252")
    # cars_df = preprocess_cars2025(cars_df)
    # performance_vs_price_bubbles(cars_df)

    # -------- Preprocess recall data for viz3 + viz4 --------
    recall_path = "data/recall"
    recall_df = preprocess_recall_data(recall_path)

    # -------- Visualization 3 (placeholder for now) --------
    viz3(recall_df)

    # -------- Visualization 4: interactive PyQt6 window --------
    app = QApplication(sys.argv)
    window = viz4(recall_df)  # returns RecallTrendsWindow
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
