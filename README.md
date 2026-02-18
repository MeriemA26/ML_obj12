# EquiNourish: Predictive Food Equity Engine

> **Foreseeing Needs. Empowering Communities.**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

**EquiNourish** is a next-generation predictive intelligence platform dedicated to solving the food security crisis. By synthesizing socioeconomic data, health metrics, and infrastructure analytics, we provide a crystal-clear view of the **food environment landscape**—today and tomorrow.

Our mission? To turn raw data into **lifelines** for vulnerable communities.

---

## The Intelligence Core (Objectives)

### 1. QualitySense (`food_quality`)
***"Is the food good enough?"***
*Objective: Hyper-local Food Quality Assessment*

We don't just guess; we **know**. Using a sophisticated **Random Forest Regressor**, QualitySense triangulates income, activity levels, and resource access to assign a definitive **Quality Score** to any region.

*   **Precision:** $R^2 \approx 0.99$
*   **Insight:** Detects subtle degradations in food quality before they become health crises.

*   **Tech Stack:** `Python`, `Scikit-Learn`, `Pandas`, `Django`
*   **Model:** Random Forest Regressor ($R^2 \approx 0.99$)
*   **Key Inputs:** Median Household Income, Physical Inactivity Rate, Food Insecurity Rate, Access to Exercise.
*   **Output:** A granular quality score (0-100) with actionable categorization (Low/Medium/High).

### 2. Food Desert Prediction (`food_desert`)
***Objective:** Proactively identify potential food deserts before they become critical.*

Using an **Optimized Random Forest Classifier**, this tool predicts the likelihood of a region becoming a food desert based on demographic and economic indicators.

*   **Tech Stack:** `Python`, `Scikit-Learn`, `Imbalanced-Learn`, `Django`
*   **Model:** Optimized Random Forest (AUC: 0.92)
*   **Key Features:** Poverty Rate, Vehicle Access, Elderly Population, Obesity Rates.
*   **Highlights:** High recall (85%) ensures vulnerable areas are rarely missed.

### 3. Customer Segmentation (`segment`)
***Objective:** Understand community demographics for targeted interventions.*

A **Support Vector Machine (SVM)** approach to segment counties/customers based on economic stability, employment, and income levels.

*   **Tech Stack:** `Python`, `Scikit-Learn` (SVM), `Matplotlib` (Visualization)
*   **Purpose:** Tailors policy and aid programs to the specific economic reality of each segment.

### 4. Future Insecurity Hotspots (`predictor`)
***Objective:** Forecast future risks of food insecurity.*

A predictive engine that models long-term trends to highlight areas at risk of declining into food insecurity, enabling preventative action.

*   **Model:** Random Forest Regressor.
*   **Focus:** Long-term socioeconomic trends and their impact on food access.

### 5. Diabetes Risk Assessment (`diabetes_risk`)
***Objective:** Correlate environmental factors with health outcomes.*

An **SVM (RBF Kernel)** model that assesses diabetes risk levels based on the food environment and lifestyle factors of a population.

---

## Technology Stack

### Backend & AI
*   **Framework:** Django 5.2 (Python)
*   **Machine Learning:** Scikit-Learn, NumPy, Pandas, Joblib
*   **Data Processing:** Excel/CSV integration, Data Normalization Pipelines

### Frontend & Visualization
*   **Templating:** Django Templates (HTML5/CSS3)
*   **Dashboards:** Power BI Integration capable
*   **Styling:** Responsive, modern UI/UX design

---

## Project Structure

```
d:/app/DATAWAREHOUSING/ML_obj12/
├── food_quality/           # Objective 1: Quality Prediction App
│   ├── ml/                 # Hosted Models (food_quality_model_final.pkl)
│   └── views.py            # Inference Logic
├── food_desert/            # Objective 2: Desert Prediction App
│   ├── ml/                 # Hosted Models (random_forest_enhanced.pkl)
│   └── views.py            # Inference Logic
├── diabetes_risk/          # Health Outcome Analysis
├── segment/                # Economic Segmentation Module
├── predictor/              # Future Hotspot Analysis
├── ml_project/             # Core Django Settings & Routing
└── manage.py               # Application Entry Point
```

## Getting Started

1.  **Environment Setup**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

3.  **Access the Modules**
    *   **Food Desert Predictor:** `http://localhost:8000/`
    *   **Food Quality Predictor:** `http://localhost:8000/quality/`
    *   **Diabetes Risk:** `http://localhost:8000/diabetes-risk/`

---

*Built for better health and smarter cities.*
