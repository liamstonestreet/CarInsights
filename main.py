import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import StringIO
import sys
import re

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
	                   "HorsePower": "horsepower",
	                   "Total Speed": "total_speed",
	                   "Performance(0 - 100 )KM/H": "performance",
	                   "Cars Prices": "price",
	                   "Fuel Types": "fuel_type",
	                   "Seats": "seats",
	                   "Torque": "torque"}, inplace=True)
	


	########## DROP DUPLICATES ##########
	# Remove duplicate rows
	print(f"Dataframe shape before dropping duplicates: {df.shape}")
	df = df.drop_duplicates()
	print(f"Dataframe shape after dropping duplicates: {df.shape}")

	########## CONVERTING PRICE RANGES TO EXACT NUMERICS ##########
	# Clean numeric extraction
	# df["price"] = df["price"].str.replace(r"[�]", "111111111", regex=True)
	# df["price"] = df["price"].str.replace(r"[^0-9\-]", "", regex=True)
	# #df["price"] = df["price"].replace("", 0)  # Replace empty strings with 0

	# # Compute average and plus/minus values
	# def process_price(p):
	# 	p = str(p)
	# 	if "-" in p:
	# 		low, high = map(int, p.split("-"))
	# 		avg = (low + high) / 2
	# 		diff = abs(high - low) / 2 # plus/minus value
	# 	else:
	# 		print(f"Processing single price: '{p}'")
	# 		avg = int(p)
	# 		diff = 0
	# 	return avg, diff

	# df[["price_avg", "price_plusminus"]] = df["price"].apply(
	# 	lambda x: pd.Series(process_price(x))
	# )

	# Strip extra spaces
	for col in df.select_dtypes(include="object").columns:
		df.loc[:, col] = df[col].str.strip()

	# Handle ranges
	def handle_range(val):
		if pd.isna(val):
			return np.nan
		s = str(val).replace(",", "")
		nums = re.findall(r"\d+\.?\d*", s)
		if len(nums) == 0:
			return np.nan
		nums = list(map(float, nums))
		return np.mean(nums)
	
	# Clean
	df.loc[:, "battery_capacity"] = df["battery_capacity"].astype(str).str.replace("cc","", regex=False)
	df.loc[:, "battery_capacity"] = df["battery_capacity"].apply(handle_range)

	df.loc[:, "horsepower"] = df["horsepower"].astype(str).str.replace("hp","", regex=False)
	df.loc[:, "horsepower"] = df["horsepower"].apply(handle_range)

	df.loc[:, "total_speed"] = df["total_speed"].astype(str).str.replace("km/h","", regex=False)
	df.loc[:, "total_speed"] = df["total_speed"].apply(handle_range)

	df.loc[:, "performance"] = df["performance"].astype(str).str.replace("sec","", regex=False)
	df.loc[:, "performance"] = df["performance"].apply(handle_range)

	df.loc[:, "price"] = df["price"].astype(str).str.replace("USD","", regex=False).str.replace("usd","", regex=False).str.replace("$", "", regex=False)
	df.loc[:, "price"] = df["price"].apply(handle_range)

	df.loc[:, "torque"] = df["torque"].astype(str).str.replace("Nm","", regex=False)
	df.loc[:, "torque"] = df["torque"].apply(handle_range)

	df.reset_index(drop=True, inplace=True)

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

def brand_box_sidebyside(df, brands=["Nissan", "Volkswagen", "Porsche", "Mazda", "Mitsubishi"]):
	# brands = df['brand'].value_counts().index[:5]
	fig, axes = plt.subplots(1, 5, figsize=(20, 5))
	for i, brand in enumerate(brands):
		if brand not in df['brand'].values:
			print(f"[Boxplot Function] >> Brand '{brand}' not found in dataframe. Continuing...")
			continue
		brand_data = df[df['brand'] == brand]['price']
		axes[i].boxplot(brand_data.dropna())
		axes[i].set_title(brand)
		axes[i].set_ylabel('Price (AVG)')

	# Adjust spacing between subplots
	# fig.subplots_adjust(wspace=0.3)

	plt.tight_layout()
	plt.show()

if __name__ == "__main__":
	main()