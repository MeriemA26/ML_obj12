"""Quick test to check model probability range"""
import joblib
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Load model and scaler
model = joblib.load('diabetes_risk/ml_models/diabetes_svm_model (1).pkl')
scaler = joblib.load('diabetes_risk/ml_models/diabetes_scaler (1).pkl')

print("="*50)
print("DIABETES MODEL DIAGNOSTIC")
print("="*50)
print(f"Model classes: {model.classes_}")
print(f"Support vectors per class: {model.n_support_}")
print(f"Scaler features: {scaler.n_features_in_}")
print(f"Scaler means: {scaler.mean_}")
print("="*50)

# Test with extreme values 
# 18 features: obesity, inactivity, exercise, income, poverty, food_insec, snap, nslp, ff, super, laccess, uninsured, pcp, seniors, medinc, soda, milk, rec

# Extreme HIGH risk scenario
high_risk = np.array([[
    0.60,    # obesity (60%)
    0.50,    # inactivity (50%)
    0.10,    # exercise access (10% - very low)
    15000,   # median income (low)
    50.0,    # poverty rate (50%)
    0.50,    # food insecurity (50%)
    50.0,    # SNAP (50%)
    30.0,    # NSLP 
    2.0,     # fast food
    0.001,   # supercenters
    100000,  # low access pop
    0.50,    # uninsured (50%)
    10,      # physicians per 100k (low)
    30.0,    # seniors %
    15000,   # MEDHHINC
    4.0,     # soda price
    4.0,     # milk price
    0.001    # rec facilities
]])

# Extreme LOW risk scenario
low_risk = np.array([[
    0.15,    # obesity (15%)
    0.10,    # inactivity (10%)
    0.90,    # exercise access (90%)
    100000,  # median income (high)
    5.0,     # poverty rate (5%)
    0.05,    # food insecurity (5%)
    3.0,     # SNAP (3%)
    5.0,     # NSLP
    0.2,     # fast food
    0.1,     # supercenters
    500,     # low access pop
    0.05,    # uninsured (5%)
    100,     # physicians per 100k (high)
    10.0,    # seniors %
    100000,  # MEDHHINC
    2.0,     # soda price
    2.0,     # milk price
    0.2      # rec facilities
]])

print("\nTesting HIGH RISK scenario:")
X_scaled = scaler.transform(high_risk)
prob = model.predict_proba(X_scaled)
print(f"  Class 0 (no diabetes): {prob[0][0]:.4f}")
print(f"  Class 1 (diabetes): {prob[0][1]:.4f}")

print("\nTesting LOW RISK scenario:")
X_scaled = scaler.transform(low_risk)
prob = model.predict_proba(X_scaled)
print(f"  Class 0 (no diabetes): {prob[0][0]:.4f}")
print(f"  Class 1 (diabetes): {prob[0][1]:.4f}")

# Find what values give max probability
print("\n" + "="*50)
print("SEARCHING FOR MAX PROBABILITY INPUT...")
max_prob = 0
best_input = None

for _ in range(1000):
    # Random extreme values
    test = np.random.uniform(low=[0.5, 0.5, 0.01, 10000, 30, 0.3, 20, 5, 0.5, 0.001, 10000, 0.3, 5, 10, 10000, 2, 2, 0.001],
                              high=[0.8, 0.8, 0.2, 30000, 60, 0.6, 40, 40, 3, 0.1, 200000, 0.6, 50, 40, 40000, 5, 5, 0.1],
                              size=(1, 18))
    X_s = scaler.transform(test)
    p = model.predict_proba(X_s)[0][1]
    if p > max_prob:
        max_prob = p
        best_input = test

print(f"Max probability found: {max_prob:.4f} ({max_prob*100:.1f}%)")
