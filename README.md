# CS 439: Final Project

Coded and completed by Liam Stonestreet, Aaron, and Shane Liu.

## File Structure

Data is in `data/` directory.

## Objective
Most car search tools only provide surface-level information such as price, mileage, and basic specifications. This project integrates car specifications to create a **Performance vs. Price Explorer**, helping consumers visualize tradeoffs between affordability and performance across brands and models.

## Data Source
- **Cars Dataset 2025 (European Market)**  
  Kaggle: [abdulmalik1518/cars-datasets-2025](https://www.kaggle.com/datasets/abdulmalik1518/cars-datasets-2025)  
  Features: brand, model, engine, horsepower, top speed, acceleration (0–100 km/h), price (USD), fuel type, seating capacity, torque.

## File Structure
- `main.py` → orchestrates preprocessing + visualization  
- `preprocess.py` → cleans and standardizes dataset  
- `visualize.py` → contains plotting functions  
- `download_data.py` → downloads Kaggle dataset  
- `data/` → raw datasets  
- `output/` → saved plots  

## Visualization 1: Performance vs. Price Explorer
- **Design**: Three bubble charts side-by-side  
- **X-axis**: Price (USD)  
- **Y-axis**: Horsepower, Acceleration, Top Speed (one per chart)  
- **Bubble size**: Seating capacity  
- **Bubble color**: Fuel type (Petrol, Diesel, Hybrid, Electric)  
- **Tooltip details**: Model, company, torque, acceleration, top speed  

---

## Visualization 3: Interactive Recall Trends (Make + Model)
An interactive PyQt6 tool that visualizes recall frequency over time.

- **Dropdown 1**: Select car **Make**  
- **Dropdown 2**: Select **Model** or “All models”  
- **X-axis**: Model Year (formatted as `'YY` or `YY`)  
- **Y-axis**: Number of distinct recall campaigns  
- **Behavior**: Missing years automatically filled with zero; y-axis uses whole numbers only  
- **Purpose**: Allows users to compare how different brands and models trend in recall activity over the years  

---

## Visualization 4: Recall Summary Wordcloud
Creates a wordcloud from the **SUMMARY** field in the NHTSA recall dataset to highlight the most frequently occurring terms across all safety recall notices.

- **Input**: Free-text recall summaries  
- **Processing**: Removes stopwords and common filler terms  
- **Output**: `output/recall_wordcloud.png`  
- **Purpose**: Reveals recurring themes such as airbags, fuel systems, fires, and steering issues  

---