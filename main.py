import pandas as pd
from preprocess import preprocess_cars2025
from visualize import performance_vs_price_bubbles

def main():
	path = "data/cars_2025.csv"
	df = pd.read_csv(path, encoding="cp1252")
	df = preprocess_cars2025(df)
	performance_vs_price_bubbles(df)

if __name__ == "__main__":
	main()
