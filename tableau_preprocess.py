import pandas as pd
import numpy as np
import re

def preprocess_cars2025(df):
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

    df = df.drop_duplicates().copy()

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
                return np.nan

        # Case 2: numeric ranges or single values
        nums = re.findall(r"\d+\.?\d*", s)
        if not nums:
            return np.nan
        return np.mean(list(map(float, nums)))

    df["horsepower"] = df["horsepower"].astype(str).str.replace("hp", "", regex=False).apply(handle_range)
    df["total_speed"] = df["total_speed"].astype(str).str.replace("km/h", "", regex=False).apply(handle_range)
    df["performance"] = df["performance"].astype(str).str.replace("sec", "", regex=False).apply(handle_range)
    df["price"] = df["price"].astype(str).str.replace("USD", "", regex=False).str.replace("$", "", regex=False).apply(handle_range)
    df["seats"] = df["seats"].apply(handle_range)
    df["torque"] = df["torque"].astype(str).str.replace("Nm", "", regex=False).apply(handle_range)
    df["battery_capacity"] = df["battery_capacity"].astype(str).str.replace("cc", "", regex=False).apply(handle_range)

    numeric_cols = ["price", "horsepower", "performance", "total_speed", "seats", "torque", "battery_capacity"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    df = df[df["seats"].notna() & (df["seats"] > 0)]
    df = df[df["price"].notna() & (df["price"] > 0)]

    df["fuel_type"] = df["fuel_type"].astype(str).str.strip().str.title()
    valid_types = ["Petrol", "Diesel", "Hybrid", "Electric"]
    df = df[df["fuel_type"].isin(valid_types)]

    df = df[df["brand"].notna() & df["model"].notna()]
    df = df[df["brand"].str.strip() != ""]
    df = df[df["model"].str.strip() != ""]
    df = df[~df["model"].astype(str).str.strip().eq("*")]

    return df

def build_radar_dataset(df):
    metrics = ["price", "total_speed", "performance", "horsepower", "torque"]

    mean_df = df.groupby("fuel_type")[metrics].mean().reset_index()
    median_df = df.groupby("fuel_type")[metrics].median().reset_index()

    mean_df["aggregation"] = "mean"
    median_df["aggregation"] = "median"

    combined = pd.concat([mean_df, median_df], ignore_index=True)

    # Normalize each metric separately (so polygons are comparable)
    for m in metrics:
        min_val = combined[m].min()
        max_val = combined[m].max()
        combined[m] = (combined[m] - min_val) / (max_val - min_val) if max_val > min_val else 0

    metric_angles = {
        "price": 0,
        "total_speed": 2*np.pi/5,       # 72°
        "performance": 2*2*np.pi/5,     # 144°
        "horsepower": 3*2*np.pi/5,      # 216°
        "torque": 4*2*np.pi/5           # 288°
    }

    radar_df = combined.melt(id_vars=["fuel_type","aggregation"], value_vars=metrics,
                             var_name="metric", value_name="value")
    radar_df["angle"] = radar_df["metric"].map(metric_angles)
    radar_df["x"] = radar_df["value"] * np.cos(radar_df["angle"])
    radar_df["y"] = radar_df["value"] * np.sin(radar_df["angle"])

    return radar_df

def main():
    raw_df = pd.read_csv("data/cars252_global.csv", encoding="cp1252")

    df = preprocess_cars2025(raw_df)

    df.to_csv("scatterplot_data.csv", index=False)
    print("Scatterplot dataset exported to scatterplot_data.csv")

    radar_df = build_radar_dataset(df)
    radar_df.to_csv("fuel_type_radar.csv", index=False)
    print("Radar dataset exported to fuel_type_radar.csv")

if __name__ == "__main__":
    main()
