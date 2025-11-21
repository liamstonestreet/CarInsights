import pandas as pd
import numpy as np
import re

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
