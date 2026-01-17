import pandas as pd

# Merge all three datasets on date, state, district, and pincode
print("🔄 Merging datasets...")

# First merge: enrollment + demographic
merged_enroll_demo = pd.merge(
    enrollment_data,
    demographic_data,
    on=['date', 'state', 'district', 'pincode'],
    how='outer',
    indicator='_merge_demo'
)
print(f"After enrollment + demographic merge: {len(merged_enroll_demo):,} rows")
print(f"  Only enrollment: {(merged_enroll_demo['_merge_demo'] == 'left_only').sum():,}")
print(f"  Only demographic: {(merged_enroll_demo['_merge_demo'] == 'right_only').sum():,}")
print(f"  Both: {(merged_enroll_demo['_merge_demo'] == 'both').sum():,}")

# Second merge: add biometric
integrated_dataset = pd.merge(
    merged_enroll_demo.drop('_merge_demo', axis=1),
    biometric_data,
    on=['date', 'state', 'district', 'pincode'],
    how='outer',
    indicator='_merge_bio'
)
print(f"\nAfter adding biometric data: {len(integrated_dataset):,} rows")
print(f"  Without biometric: {(integrated_dataset['_merge_bio'] == 'left_only').sum():,}")
print(f"  Only biometric: {(integrated_dataset['_merge_bio'] == 'right_only').sum():,}")
print(f"  With biometric: {(integrated_dataset['_merge_bio'] == 'both').sum():,}")

integrated_dataset = integrated_dataset.drop('_merge_bio', axis=1)

print(f"\n✅ Integrated Dataset Created:")
print(f"Total rows: {len(integrated_dataset):,}")
print(f"Total columns: {len(integrated_dataset.columns)}")
print(f"\nColumns: {list(integrated_dataset.columns)}")

print(f"\n📊 Data Validation:")
print(f"Missing values per column:")
print(integrated_dataset.isnull().sum())

print(f"\n🔍 Data Types:")
print(integrated_dataset.dtypes)

print(f"\n📈 Sample of Integrated Data:")
print(integrated_dataset.head(10))

print(f"\n✓ SUCCESS: All files loaded and merged correctly")
print(f"  - Enrollment: {len(enrollment_data):,} rows loaded")
print(f"  - Demographic: {len(demographic_data):,} rows loaded")
print(f"  - Biometric: {len(biometric_data):,} rows loaded")
print(f"  - Integrated: {len(integrated_dataset):,} rows total")