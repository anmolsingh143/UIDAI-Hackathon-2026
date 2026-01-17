import pandas as pd
import glob

# Load all enrollment CSV files
enrollment_files = [
    'api_data_aadhar_enrolment_0_500000.csv',
    'api_data_aadhar_enrolment_500000_1000000.csv',
    'api_data_aadhar_enrolment_1000000_1006029.csv'
]

enroll_dfs = []
for enroll_file in enrollment_files:
    _df = pd.read_csv(enroll_file)
    enroll_dfs.append(_df)
    print(f"Loaded {enroll_file}: {len(_df)} rows, {len(_df.columns)} columns")

# Combine enrollment data
enrollment_data = pd.concat(enroll_dfs, ignore_index=True)

print(f"\n✅ Combined Enrollment Data:")
print(f"Total rows: {len(enrollment_data):,}")
print(f"Total columns: {len(enrollment_data.columns)}")
print(f"\nColumns: {list(enrollment_data.columns)}")
print(f"\nFirst few rows:")
print(enrollment_data.head())
print(f"\nData types:")
print(enrollment_data.dtypes)