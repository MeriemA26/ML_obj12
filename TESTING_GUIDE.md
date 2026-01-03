# ML Models Testing Guide

This document provides test values for all 8 ML objectives integrated in the DataHub application.

---

## 1. Food Desert Classification (obj2)
**URL:** `/`  
**Algorithm:** Random Forest  
**Purpose:** Classifies areas as food deserts based on socioeconomic indicators

### Test Scenario A: Healthy Area (Low Risk)
| Feature | Value |
|---------|-------|
| MEDHHINC10 | 75000 |
| Unemployment_Rate_county | 3.5 |
| Labor_Force | 50000 |
| Employed | 48000 |
| Unemployed | 2000 |
| median_household_income | 75000 |

**Expected Result:** Zone Saine / Non-Desert (Low probability)

### Test Scenario B: At-Risk Area (High Risk)
| Feature | Value |
|---------|-------|
| MEDHHINC10 | 25000 |
| Unemployment_Rate_county | 12.5 |
| Labor_Force | 30000 |
| Employed | 26000 |
| Unemployed | 4000 |
| median_household_income | 25000 |

**Expected Result:** Désert Alimentaire / Food Desert (High probability)

---

## 2. Food Quality Score (obj1)
**URL:** `/quality/`  
**Algorithm:** Random Forest Regression  
**Purpose:** Predicts food quality score based on nutritional and environmental factors

### Test Scenario A: High Quality
| Feature | Value |
|---------|-------|
| Protein | 25 |
| Fat | 10 |
| Carbohydrates | 45 |
| Fiber | 8 |
| Sugar | 5 |
| Sodium | 300 |
| Calories | 350 |
| Serving_Size | 100 |

**Expected Result:** Score > 70 (Excellent Quality)

### Test Scenario B: Low Quality
| Feature | Value |
|---------|-------|
| Protein | 5 |
| Fat | 35 |
| Carbohydrates | 60 |
| Fiber | 1 |
| Sugar | 40 |
| Sodium | 1500 |
| Calories | 600 |
| Serving_Size | 100 |

**Expected Result:** Score < 40 (Poor Quality)

---

## 3. Diabetes Risk (SVM)
**URL:** `/diabetes-risk/`  
**Algorithm:** SVM Classification  
**Purpose:** Predicts diabetes risk probability based on health and lifestyle factors

### Test Scenario A: Low Risk
| Feature | Value |
|---------|-------|
| Age | 30 |
| BMI | 22 |
| Blood_Pressure | 110 |
| Glucose | 85 |
| Physical_Activity | 5 |
| Family_History | 0 |
| Income | 60000 |
| Education_Level | 4 |

**Expected Result:** Low Risk (< 20% probability)

### Test Scenario B: High Risk
| Feature | Value |
|---------|-------|
| Age | 55 |
| BMI | 32 |
| Blood_Pressure | 145 |
| Glucose | 130 |
| Physical_Activity | 1 |
| Family_History | 1 |
| Income | 25000 |
| Education_Level | 2 |

**Expected Result:** High Risk (> 60% probability)

---

## 4. Obesity Risk (XGBoost)
**URL:** `/obesity/`  
**Algorithm:** XGBoost Classification  
**Purpose:** Predicts obesity level classification

### Test Scenario A: Normal Weight
| Feature | Value |
|---------|-------|
| Age | 28 |
| Height | 1.75 |
| Weight | 68 |
| family_history_with_overweight | 0 |
| FAVC (Freq high caloric food) | 0 |
| FCVC (Freq vegetables) | 3 |
| NCP (Num main meals) | 3 |
| CAEC (Eating between meals) | Sometimes |
| SMOKE | 0 |
| CH2O (Water daily) | 2.5 |
| SCC (Calorie monitoring) | 1 |
| FAF (Physical activity freq) | 3 |
| TUE (Technology usage) | 1 |
| CALC (Alcohol consumption) | Sometimes |
| MTRANS (Transportation) | Walking |

**Expected Result:** Normal Weight

### Test Scenario B: Obesity Type II
| Feature | Value |
|---------|-------|
| Age | 45 |
| Height | 1.65 |
| Weight | 105 |
| family_history_with_overweight | 1 |
| FAVC | 1 |
| FCVC | 1 |
| NCP | 4 |
| CAEC | Always |
| SMOKE | 0 |
| CH2O | 1 |
| SCC | 0 |
| FAF | 0 |
| TUE | 3 |
| CALC | Frequently |
| MTRANS | Automobile |

**Expected Result:** Obesity Type II

---

## 5. Customer Segmentation (SVM)
**URL:** `/segment/`  
**Algorithm:** SVM Classification  
**Purpose:** Segments customers based on economic indicators

### Test Scenario A: High-Value Segment
| Feature | Value |
|---------|-------|
| MEDHHINC10 | 85000 |
| Unemployment_Rate_county | 2.5 |
| Labor_Force | 60000 |
| Employed | 58500 |
| Unemployed | 1500 |
| median_household_income | 85000 |

**Expected Result:** Segment 3 or 4 (High-Value)

### Test Scenario B: Budget Segment
| Feature | Value |
|---------|-------|
| MEDHHINC10 | 32000 |
| Unemployment_Rate_county | 9.0 |
| Labor_Force | 25000 |
| Employed | 22750 |
| Unemployed | 2250 |
| median_household_income | 32000 |

**Expected Result:** Segment 0 or 1 (Budget-Conscious)

---

## 6. Limited Access Population (KNN)
**URL:** `/access/`  
**Algorithm:** KNN Regression  
**Purpose:** Predicts population with limited food access

### Test Scenario A: Good Access (Low Limited Population)
| Feature | Value |
|---------|-------|
| Supercenters Count | 15 |
| Households Without Vehicle | 100 |
| Employed Population | 50000 |
| Labor Force Size | 52000 |
| Fast Food Restaurants | 30 |
| Full-Service Restaurants | 25 |
| Grocery Stores Count | 25 |
| Unemployed Population | 2000 |
| Hispanic Population % | 10 |
| SNAP Participation Rate % | 5 |
| Non-Hispanic White % | 75 |
| Adult Obesity Rate % | 22 |
| WIC Participation % | 4 |
| Exercise Access % | 85 |
| Median Household Income | 80000 |

**Expected Result:** < 5,000 (Low Limited Access)

### Test Scenario B: Poor Access (High Limited Population)
| Feature | Value |
|---------|-------|
| Supercenters Count | 0 |
| Households Without Vehicle | 3000 |
| Employed Population | 15000 |
| Labor Force Size | 20000 |
| Fast Food Restaurants | 5 |
| Full-Service Restaurants | 2 |
| Grocery Stores Count | 2 |
| Unemployed Population | 5000 |
| Hispanic Population % | 40 |
| SNAP Participation Rate % | 25 |
| Non-Hispanic White % | 30 |
| Adult Obesity Rate % | 38 |
| WIC Participation % | 18 |
| Exercise Access % | 30 |
| Median Household Income | 28000 |

**Expected Result:** > 50,000 (High Limited Access)

---

## 7. Health Score (RF)
**URL:** `/predictor/`  
**Algorithm:** Random Forest Regression  
**Purpose:** Predicts overall health risk score for an area

### Test Scenario A: Low Risk Area
| Feature | Value |
|---------|-------|
| Median Household Income ($) | 75000 |
| Child Poverty Rate (%) | 8 |
| Physical Inactivity Rate (%) | 15 |
| Food Access Score (0-10) | 8 |
| Poverty Rate (%) | 8 |
| SNAP Participation (%) | 5 |
| Diabetes Prevalence (%) | 6 |
| Food Environment Index (0-10) | 8.5 |

**Expected Result:** Score < 0.3 (Low Risk)

### Test Scenario B: High Risk Area
| Feature | Value |
|---------|-------|
| Median Household Income ($) | 28000 |
| Child Poverty Rate (%) | 35 |
| Physical Inactivity Rate (%) | 35 |
| Food Access Score (0-10) | 3 |
| Poverty Rate (%) | 30 |
| SNAP Participation (%) | 22 |
| Diabetes Prevalence (%) | 15 |
| Food Environment Index (0-10) | 3.5 |

**Expected Result:** Score > 0.6 (High Risk)

---

## 8. Store Impact on Health (KNN)
**URL:** `/predictor/store/`  
**Algorithm:** KNN Classification  
**Purpose:** Predicts health impact based on store availability

### Test Scenario A: Positive Impact (Healthy Environment)
| Feature | Value |
|---------|-------|
| Fast-Food Restaurants Count | 10 |
| Fast-Food per 1000 Pop | 0.2 |
| Supermarkets Count | 20 |
| Supermarkets per 1000 Pop | 0.4 |
| Farmers Markets Count | 8 |
| Farmers Markets per 1000 | 0.15 |
| Markets Accepting SNAP (%) | 75 |
| Limited Access Population | 2000 |
| Low Income Limited Access | 500 |
| No Vehicle Limited Access | 100 |
| Food Access Score (0-10) | 8 |
| Food Environment Index | 8 |
| Median Income ($) | 70000 |
| Poverty Rate (%) | 8 |
| Food Insecurity Rate (%) | 6 |
| SNAP Participation (%) | 5 |

**Expected Result:** Low Risk / Healthy Environment

### Test Scenario B: Negative Impact (Unhealthy Environment)
| Feature | Value |
|---------|-------|
| Fast-Food Restaurants Count | 80 |
| Fast-Food per 1000 Pop | 1.5 |
| Supermarkets Count | 3 |
| Supermarkets per 1000 Pop | 0.05 |
| Farmers Markets Count | 0 |
| Farmers Markets per 1000 | 0 |
| Markets Accepting SNAP (%) | 10 |
| Limited Access Population | 25000 |
| Low Income Limited Access | 12000 |
| No Vehicle Limited Access | 4000 |
| Food Access Score (0-10) | 2 |
| Food Environment Index | 2.5 |
| Median Income ($) | 25000 |
| Poverty Rate (%) | 28 |
| Food Insecurity Rate (%) | 22 |
| SNAP Participation (%) | 20 |

**Expected Result:** High Risk / Unhealthy Environment

---

## Quick Reference - URLs

| # | Model | URL |
|---|-------|-----|
| 1 | Food Desert | http://127.0.0.1:8000/ |
| 2 | Food Quality | http://127.0.0.1:8000/quality/ |
| 3 | Diabetes Risk | http://127.0.0.1:8000/diabetes-risk/ |
| 4 | Obesity Risk | http://127.0.0.1:8000/obesity/ |
| 5 | Segmentation | http://127.0.0.1:8000/segment/ |
| 6 | Limited Access | http://127.0.0.1:8000/access/ |
| 7 | Health Score | http://127.0.0.1:8000/predictor/ |
| 8 | Store Impact | http://127.0.0.1:8000/predictor/store/ |

---

*Last Updated: January 3, 2026*
