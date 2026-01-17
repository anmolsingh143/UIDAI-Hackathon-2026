import pandas as pd

# Load all demographic CSV files
demographic_files = [
    'api_data_aadhar_demographic_0_500000.csv',
    'api_data_aadhar_demographic_500000_1000000.csv',
    'api_data_aadhar_demographic_1000000_1500000.csv',
    'api_data_aadhar_demographic_1500000_2000000.csv',
    'api_data_aadhar_demographic_2000000_2071700.csv'
]

demo_dfs = []
for demo_file in demographic_files:
    _df = pd.read_csv(demo_file)
    demo_dfs.append(_df)
    print(f"Loaded {demo_file}: {len(_df)} rows, {len(_df.columns)} columns")

# Combine demographic data
demographic_data = pd.concat(demo_dfs, ignore_index=True)

print(f"\n✅ Combined Demographic Data:")
print(f"Total rows: {len(demographic_data):,}")
print(f"Total columns: {len(demographic_data.columns)}")
print(f"\nColumns: {list(demographic_data.columns)}")
print(f"\nFirst few rows:")
print(demographic_data.head())
print(f"\nData types:")
print(demographic_data.dtypes)