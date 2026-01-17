import pandas as pd

# Load all biometric CSV files
biometric_files = [
    'api_data_aadhar_biometric_0_500000.csv',
    'api_data_aadhar_biometric_500000_1000000.csv',
    'api_data_aadhar_biometric_1000000_1500000.csv',
    'api_data_aadhar_biometric_1500000_1861108.csv'
]

bio_dfs = []
for bio_file in biometric_files:
    _df = pd.read_csv(bio_file)
    bio_dfs.append(_df)
    print(f"Loaded {bio_file}: {len(_df)} rows, {len(_df.columns)} columns")

# Combine biometric data
biometric_data = pd.concat(bio_dfs, ignore_index=True)

print(f"\n✅ Combined Biometric Data:")
print(f"Total rows: {len(biometric_data):,}")
print(f"Total columns: {len(biometric_data.columns)}")
print(f"\nColumns: {list(biometric_data.columns)}")
print(f"\nFirst few rows:")
print(biometric_data.head())
print(f"\nData types:")
print(biometric_data.dtypes)