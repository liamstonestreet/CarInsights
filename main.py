import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import StringIO
import sys
import re



def preprocess_india_cars(df):
	# TODO
	return df

def preprocess_safety_ratings(df):
	# TODO
	return df

def preprocess_recalls_2025(df):
	# TODO
	return df

def preprocess_cars2025(df):
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
	path1 = "data/cars/cars_2025.csv"
	path2 = "data/cars/cars_us_sales_2023.csv"
	path3 = "data/cars/safety_ratings.csv"
	path4 = "data/cars/recalls_2025.csv"
	cars_2025_df = pd.read_csv(path1, encoding='cp1252')
	cars_2025_df = preprocess_cars2025(cars_2025_df)

	us_sales_df = pd.read_csv(path2)
	us_sales_df = preprocess_india_cars(us_sales_df)

	safety_ratings_df = pd.read_csv(path3, low_memory=False)
	safety_ratings_df = preprocess_safety_ratings(safety_ratings_df)

	recalls_2025_df = pd.read_csv(path4)
	recalls_2025_df = preprocess_recalls_2025(recalls_2025_df)

	# Debug output
	print("Cars 2025 DataFrame Columns:")
	print(len(safety_ratings_df.columns))
	print(safety_ratings_df.columns)

	print("US Sales DataFrame Columns:")
	print(len(us_sales_df.columns))
	print(us_sales_df.columns)

	print("Recalls 2025 DataFrame Columns:")
	print(len(recalls_2025_df.columns))
	print(recalls_2025_df.columns)

	# Quick sanity output
	# print("Loaded dataframe — showing first 5 rows:")
	# print(df.head())
	# print("\nDataFrame info:")
	# cars_2025_df.info()
	# print("\nUnique brands:", cars_2025_df['brand'].nunique()) # 37 unique brands

	# Visualizations
	# brand_box_sidebyside(cars_2025_df)

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