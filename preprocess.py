import pandas as pd
import numpy as np
import re
import os

def preprocess_cars2025(df):
    # --- Rename columns for consistency ---
    df = df.rename(columns={
        "Company Names": "brand",
        "Cars Names": "model",
        "Engines": "engine",
        "CC/Battery Capacity": "battery_capacity",
        "HorsePower": "horsepower",
        "Total Speed": "total_speed",
        "Performance(0 - 100 )KM/H": "performance",
        "Cars Prices": "price",
        "Fuel Types": "fuel_type",
        "Seats": "seats",
        "Torque": "torque"
    })

    # --- Remove duplicates and work on a copy ---
    df = df.drop_duplicates().copy()

    # --- Helper to handle ranges and arithmetic ---
    def handle_range(val):
        if pd.isna(val):
            return np.nan
        s = str(val).replace(",", "").strip()

        # Case 1: arithmetic like "2 + 2"
        if "+" in s:
            try:
                parts = [float(x) for x in s.split("+")]
                return sum(parts)
            except Exception:
                pass

        # Case 2: numeric ranges or single values
        nums = re.findall(r"\d+\.?\d*", s)
        if not nums:
            return np.nan
        return np.mean(list(map(float, nums)))

    # --- Clean numeric columns ---
    df["horsepower"] = df["horsepower"].astype(str).str.replace("hp", "", regex=False).apply(handle_range)
    df["total_speed"] = df["total_speed"].astype(str).str.replace("km/h", "", regex=False).apply(handle_range)
    df["performance"] = df["performance"].astype(str).str.replace("sec", "", regex=False).apply(handle_range)
    df["price"] = df["price"].astype(str).str.replace("USD", "", regex=False).str.replace("$", "", regex=False).apply(handle_range)
    df["seats"] = df["seats"].apply(handle_range)
    df["torque"] = df["torque"].astype(str).str.replace("Nm", "", regex=False).apply(handle_range)
    df["battery_capacity"] = df["battery_capacity"].astype(str).str.replace("cc", "", regex=False).apply(handle_range)

    # --- Convert all numeric columns to floats ---
    numeric_cols = ["price", "horsepower", "performance", "total_speed", "seats", "torque", "battery_capacity"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # --- Handle seats specifically ---
    df["seats"] = df["seats"].fillna(0)  # you can drop instead if preferred

    # --- Clean fuel_type ---
    df["fuel_type"] = df["fuel_type"].astype(str).str.strip().str.title()
    valid_types = ["Petrol", "Diesel", "Hybrid", "Electric"]
    df.loc[~df["fuel_type"].isin(valid_types), "fuel_type"] = "Unknown"

    return df

# datasource 4
def preprocess_recall_data(recall_path):
    # combine all csv files inside the folder path "recall_path"
    df = pd.concat([pd.read_csv(os.path.join(recall_path, f)) 
                    for f in os.listdir(recall_path) 
                    if f.endswith('.csv')], 
                    ignore_index=True
                  )
    # columns: "NHTSA ID","DOCUMENT NAME","MAKE","MODEL","MODEL YEAR","SUMMARY"
    # convert columns to their respective types
    df["NHTSA ID"] = df["NHTSA ID"].astype(str).str.strip()
    df["DOCUMENT NAME"] = df["DOCUMENT NAME"].astype(str).str.strip()
    df["MAKE"] = df["MAKE"].astype(str).str.strip()
    df["MODEL"] = df["MODEL"].astype(str).str.strip()
    df["MODEL YEAR"] = pd.to_numeric(df["MODEL YEAR"], errors="coerce")
    df["SUMMARY"] = df["SUMMARY"].astype(str).str.strip()
    # remove duplicates
    df = df.drop_duplicates().copy()
    # remove all rows where "MODEL YEAR" is 9999 or NaN
    df = df[df["MODEL YEAR"].notna() & (df["MODEL YEAR"] != 9999)]

    return df
