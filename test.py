import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import StringIO
import sys

# import kagglehub
# Download latest version
# path = kagglehub.dataset_download("abdulmalik1518/cars-datasets-2025")
# print("Path to dataset files:", path)

def main():
	path = "cars_2025.csv"
	# try:
	# 	df = read_csv_with_fallback(path)
	# except Exception as e:
	# 	print("Failed to load CSV:", e, file=sys.stderr)
	# 	sys.exit(1)
	df = pd.read_csv(path, encoding='cp1252')

	# Quick sanity output
	print("Loaded dataframe — showing first 5 rows:")
	print(df.head())
	print("\nDataFrame info:")
	df.info()


if __name__ == "__main__":
	main()