import pandas as pd
import requests
import time  # For rate limiting

df = pd.read_csv('data/large_illinois_dataset.csv', low_memory=False)  # Your 5.36GB file

# clean nans or none or invalid vins
df = df[df['vin'].notna() & (df['vin'] != 'NONE')].copy()
print(f"Cleaning done! {len(df)} valid VINs found.")

print("Starting VIN decoding...")
def decode_vin(vin):
    try:
        try:
            url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{vin}?format=json"
            resp = requests.get(url, timeout=5)
            data = resp.json()['Results']
            make = next((d['Value'] for d in data if d['Variable'] == 'Make'), 'Unknown')
            model = next((d['Value'] for d in data if d['Variable'] == 'Model'), 'Unknown')
            year = next((d['Value'] for d in data if d['Variable'] == 'ModelYear'), 'Unknown')
            print(f"Processed: {make} - {model} - {year}")
            return f"{make};{model};{year}"
        except:
            return 'Decode failed'
        finally:
            time.sleep(0.01)  # Avoid rate limits (~5/sec)
    except KeyboardInterrupt:
        print("Decoding interrupted by user. Saving to file...")
        df.to_csv('dataset_with_models.csv', index=False)
        exit()

# df['decoded'] = df['vin'].apply(lambda vin: decode_vin(vin))
# Batch process in chunks for 5M+ rows
df['make_model_year'] = df['vin'].apply(decode_vin)
df.to_csv('dataset_with_models.csv', index=False)
