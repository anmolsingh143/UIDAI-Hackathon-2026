import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

print("🚀 TRAIN-TEST SPLIT AND DATA PREPARATION")
print("=" * 60)

# ===================================================================
# 1. SELECT MODELING FEATURES
# ===================================================================
print("\n📋 Selecting features for modeling...")
print("-" * 60)

# Define feature columns (exclude target and non-feature columns)
feature_columns = [
    # Temporal features
    'day_of_week', 'day_of_month', 'week_of_year', 'is_weekend', 
    'is_month_start', 'is_month_end',
    
    # Original enrollment counts
    'age_0_5', 'age_5_17', 'age_18_greater',
    'demo_age_5_17', 'demo_age_17_',
    'bio_age_5_17', 'bio_age_17_',
    
    # Aggregated enrollment metrics
    'total_enrollment', 'total_demographic', 'total_biometric', 
    'total_all_enrollments',
    
    # Age group indicators and proportions
    'has_age_0_5', 'has_age_5_17_enroll', 'has_age_18_plus',
    'pct_age_0_5', 'pct_age_5_17', 'pct_age_18_plus', 
    'num_age_groups_covered',
    
    # Biometric completeness
    'bio_completeness_score', 'bio_to_demo_ratio', 'bio_to_enroll_ratio',
    
    # Regional features (state-level, district-level, pincode-level)
    'state_enrollment_rate', 'state_avg_enrollments', 'state_record_count',
    'district_enrollment_rate', 'pincode_enrollment_rate',
    
    # Data quality indicators
    'data_types_present', 'is_partial_enrollment', 'has_zero_enrollments',
    
    # Helper indicators
    'has_enrollment', 'has_demographic', 'has_biometric'
]

# Categorical features to encode
categorical_features = ['state', 'district']

print(f"✓ Selected {len(feature_columns)} numerical features")
print(f"✓ Selected {len(categorical_features)} categorical features")

# ===================================================================
# 2. ENCODE CATEGORICAL VARIABLES
# ===================================================================
print("\n🔤 Encoding categorical variables...")
print("-" * 60)

modeling_data = modeling_df.copy()

# Label encode state and district
state_encoder = LabelEncoder()
district_encoder = LabelEncoder()

modeling_data['state_encoded'] = state_encoder.fit_transform(modeling_data['state'].astype(str))
modeling_data['district_encoded'] = district_encoder.fit_transform(modeling_data['district'].astype(str))

print(f"✓ Encoded 'state' → state_encoded ({modeling_data['state_encoded'].nunique()} unique values)")
print(f"✓ Encoded 'district' → district_encoded ({modeling_data['district_encoded'].nunique()} unique values)")

# Add encoded features to feature list
feature_columns.extend(['state_encoded', 'district_encoded'])

# ===================================================================
# 3. PREPARE X AND y
# ===================================================================
print("\n🎯 Preparing X (features) and y (target)...")
print("-" * 60)

# Target variable
y = modeling_data['enrollment_complete'].values

# Feature matrix
X = modeling_data[feature_columns].copy()

# Handle any remaining NaN values (fill with 0 or appropriate value)
print(f"\nChecking for missing values in features:")
missing_counts = X.isnull().sum()
if missing_counts.sum() > 0:
    print(f"  Found {missing_counts.sum()} missing values across features")
    print(f"  Filling missing values with 0...")
    X = X.fillna(0)
else:
    print(f"  ✓ No missing values detected")

print(f"\n✓ Feature matrix shape: {X.shape}")
print(f"✓ Target shape: {y.shape}")
print(f"✓ Total features: {X.shape[1]}")

# ===================================================================
# 4. TRAIN-TEST SPLIT
# ===================================================================
print("\n✂️  Splitting data into train and test sets...")
print("-" * 60)

# 80-20 train-test split with stratification
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y  # Maintain class distribution
)

print(f"✓ Train set: {X_train.shape[0]:,} samples ({X_train.shape[0]/len(X)*100:.1f}%)")
print(f"✓ Test set:  {X_test.shape[0]:,} samples ({X_test.shape[0]/len(X)*100:.1f}%)")

print(f"\nTarget distribution in train set:")
print(f"  Complete (1): {y_train.sum():,} ({y_train.mean()*100:.2f}%)")
print(f"  Incomplete (0): {(1-y_train).sum():,} ({(1-y_train.mean())*100:.2f}%)")

print(f"\nTarget distribution in test set:")
print(f"  Complete (1): {y_test.sum():,} ({y_test.mean()*100:.2f}%)")
print(f"  Incomplete (0): {(1-y_test).sum():,} ({(1-y_test.mean())*100:.2f}%)")

# ===================================================================
# 5. FEATURE STATISTICS
# ===================================================================
print("\n📊 Feature Statistics Summary...")
print("-" * 60)

print(f"\nFeature value ranges (first 10 features):")
for _feat in feature_columns[:10]:
    _min_val = X[_feat].min()
    _max_val = X[_feat].max()
    _mean_val = X[_feat].mean()
    print(f"  {_feat:30s}: [{_min_val:>10.2f}, {_max_val:>10.2f}], mean={_mean_val:>10.2f}")

# ===================================================================
# SUMMARY
# ===================================================================
print("\n" + "=" * 60)
print("✅ DATA PREPARATION COMPLETE")
print("=" * 60)

print(f"\n📦 Modeling Dataset Ready:")
print(f"   Total samples: {len(X):,}")
print(f"   Total features: {X.shape[1]}")
print(f"   Train samples: {X_train.shape[0]:,}")
print(f"   Test samples: {X_test.shape[0]:,}")
print(f"   Target variable: enrollment_complete")
print(f"   Class balance: {y.mean()*100:.2f}% complete, {(1-y.mean())*100:.2f}% incomplete")

print(f"\n🎯 Ready for model training!")
print(f"   Use X_train, X_test, y_train, y_test for modeling")
print(f"   All features are numerical and properly encoded")
print(f"   No missing values present")
