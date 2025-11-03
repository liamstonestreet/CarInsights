import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import StringIO
import sys

# import kagglehub
# Download latest version
# path = kagglehub.dataset_download("abdulmalik1518/cars-datasets-2025")
# print("Path to dataset files:", path)

def preprocess_data(df):
	########### RENAMING COLUMNS ###########
	df.rename(columns={"Company Names": "brand",
	                   "Cars Names": "model",
	                   "Engines": "engine",
	                   "CC/Battery Capacity": "battery_capacity",
	                   "HorsePower": "horse_power",
	                   "Total Speed": "total_speed",
	                   "Performance(0 - 100 )KM/H": "performance",
	                   "Cars Prices": "price",
	                   "Fuel Types": "fuel_type",
	                   "Seats": "seats",
	                   "Torque": "torque"}, inplace=True)


	########## CONVERTING PRICE RANGES TO EXACT NUMERICS ##########
	# Clean numeric extraction
	df["price"] = df["price"].str.replace(r"[^0-9\-]", "", regex=True)
	df["price"] = df["price"].replace("", 0)  # Replace empty strings with 0

	# Compute average and plus/minus values
	def process_price(p):
		p = str(p)
		if "-" in p:
			low, high = map(int, p.split("-"))
			avg = (low + high) / 2
			diff = abs(high - low) / 2 # plus/minus value
		else:
			# print(f"Processing single price: '{p}'")
			avg = int(p)
			diff = 0
		return avg, diff

	df[["price_avg", "price_plusminus"]] = df["price"].apply(
		lambda x: pd.Series(process_price(x))
	)
	return df

def main():
	path = "data/cars_2025.csv"
	df = pd.read_csv(path, encoding='cp1252')
	df = preprocess_data(df)

	# Quick sanity output
	# print("Loaded dataframe — showing first 5 rows:")
	# print(df.head())
	print("\nDataFrame info:")
	df.info()
	print("\nUnique brands:", df['brand'].nunique()) # 37 unique brands

	# Visualizations
	brand_box_sidebyside(df)

def brand_box_sidebyside(df):
	brands = df['brand'].value_counts().index[:5]
	fig, axes = plt.subplots(1, 5, figsize=(20, 5))
	for i, brand in enumerate(brands):
		brand_data = df[df['brand'] == brand]['price_avg']
		axes[i].boxplot(brand_data.dropna())
		axes[i].set_title(brand)
		axes[i].set_ylabel('Price (AVG)')

	# Adjust spacing between subplots
	# fig.subplots_adjust(wspace=0.3)

	plt.tight_layout()
	plt.show()

if __name__ == "__main__":
	main()