import pandas as pd
import numpy as np
import re

def preprocess_cars2025(df):
    df.rename(columns={
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
    }, inplace=True)

    df = df.drop_duplicates()

    def handle_range(val):
        if pd.isna(val):
            return np.nan
        s = str(val).replace(",", "")
        nums = re.findall(r"\d+\.?\d*", s)
        if not nums:
            return np.nan
        return np.mean(list(map(float, nums)))

    df["horsepower"] = df["horsepower"].astype(str).str.replace("hp","", regex=False).apply(handle_range)
    df["total_speed"] = df["total_speed"].astype(str).str.replace("km/h","", regex=False).apply(handle_range)
    df["performance"] = df["performance"].astype(str).str.replace("sec","", regex=False).apply(handle_range)
    df["price"] = df["price"].astype(str).str.replace("USD","", regex=False).str.replace("$","", regex=False).apply(handle_range)
    df["seats"] = df["seats"].apply(handle_range)
    df["torque"] = df["torque"].astype(str).str.replace("Nm","", regex=False).apply(handle_range)

    return df
