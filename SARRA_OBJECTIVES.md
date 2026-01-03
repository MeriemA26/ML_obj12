# Sarra Branch Objectives

Below are the exact names and details of the two machine learning objectives integrated from the `sarra` branch.

## 1. Customer Segmentation
**App Name:** `segment`
**Model Type:** SVM (Support Vector Machine)
**File:** `segment/ml/svm_segment_model.pkl`
**Objective:** Classify customers/counties into economic segments based on employment and income data.

**Key Features:**
- `MEDHHINC10` (Median Household Income)
- `Unemployment_Rate_county`
- `Labor_Force`
- `Employed`
- `Unemployed`

## 2. Predict Future Insecurity Hotspots
**App Name:** `predictor`
**Model Type:** Random Forest Regressor
**File:** `predictor/ml/rf_model.pkl`
**Objective:** Predict future food insecurity hotspots based on socioeconomic risk factors.

**Key Features:**
- `Median Household Income`
- `Child Poverty Rate`
- `Physical Inactivity Rate`
- `Food Access Score`
- `Poverty Rate`
- `SNAP Participation`
- `Diabetes Prevalence`
- `Food Environment Index`
