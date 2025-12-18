# CS 439: Final Project

Coded and completed by Liam Stonestreet, Aaron, and Shane Liu.

## File Structure
- `preprocess.py` → cleans and standardizes dataset  
- `tableau_preprocess.py` → cleans dataset used for Tableau visualizations (Global 2025 dataset)
- `data/` → raw CSV datasets  
- `output/` → saved plots

## HOW TO RUN
1. Create a Conda (or virtual) environment with Python version 3.12.
  - For conda: `conda create -n test439 python=3.12 pip`
2. Run `pip install -r requirements.txt` to install required libraries.
3. If you are getting weird pip library/dependency errors, run the following commands in a fresh conda environment with Python version 3.12:
  - `pip install h5py typing-extensions wheel`
4. Make sure you put all the CSV files in the zip folder we attached in our project package, inside `data/` directory.
4. Now you can run visualizations 3-6 by simply running their corresponding files:
  - `viz3.py`
  - `viz4.py`
  - `viz5.py`
  - `viz5.1.py`
  - `viz6_discarded.py`
5. Visualizations 1-2 are on Tableau [at this link](https://public.tableau.com/app/profile/aaron.fernandes7527/viz/Cars_17653299483430/HorsepowerScatter).

## Visualization 1: Performance vs. Price Explorer
This visualization is on Tableau [at this link](https://public.tableau.com/app/profile/aaron.fernandes7527/viz/Cars_17653299483430/HorsepowerScatter) (the first three tabs). 
- **Design**: Three bubble charts 
- **X-axis**: Price (USD)  
- **Y-axis**: Horsepower, Acceleration, Top Speed (one per chart)  
- **Bubble size**: Seating capacity  
- **Bubble color**: Fuel type (Petrol, Diesel, Hybrid, Electric)  
- **Tooltip details**: Model, company, torque, acceleration, top speed  

---

## Visualization 2: Radar chart of Fuel-type vs Price, Torque, 0-100, Horsepower, Max Speed
This visualization is on Tableau [at this link](https://public.tableau.com/app/profile/aaron.fernandes7527/viz/Cars_17653299483430/HorsepowerScatter) (the fourth tab).


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

