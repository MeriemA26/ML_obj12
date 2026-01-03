# DataHub ML Project - Setup Guide

This guide will help you clone, set up, and run the DataHub ML project locally.

---

## 📋 Prerequisites

Before starting, make sure you have the following installed:

- **Python 3.10+** (recommended: Python 3.13 or 3.14)
- **Git**
- **pip** (Python package manager)

### Verify Installation
```bash
python --version
git --version
pip --version
```

---

## 🚀 Quick Start

### Step 1: Clone the Repository

```bash
git clone https://github.com/MeriemA26/ML_obj12.git
cd ML_obj12
```

### Step 2: Create a Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install django numpy pandas scikit-learn joblib xgboost
```

Or if there's a requirements.txt:
```bash
pip install -r requirements.txt
```

### Step 4: Run the Development Server

```bash
python manage.py runserver
```

### Step 5: Open in Browser

Navigate to: **http://127.0.0.1:8000/**

---

## 📁 Project Structure

```
ML_obj12/
├── foodenv/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── obj1/                 # Food Quality Model (RF)
├── obj2/                 # Food Desert Model (RF)
├── diabetes_risk/        # Diabetes Risk Model (SVM)
├── obesity_predictor/    # Obesity Risk Model (XGBoost)
├── segment/              # Customer Segmentation (SVM)
├── mlapp/                # Limited Access Model (KNN)
├── predictor/            # Health Score + Store Impact Models
├── templates/            # Base templates
├── static/               # CSS and static files
├── TESTING_GUIDE.md      # Test values for all models
└── manage.py             # Django management script
```

---

## 🎯 Available ML Models (8 Total)

| # | Model | URL | Algorithm |
|---|-------|-----|-----------|
| 1 | Food Desert | http://127.0.0.1:8000/ | Random Forest |
| 2 | Food Quality | http://127.0.0.1:8000/quality/ | Random Forest |
| 3 | Diabetes Risk | http://127.0.0.1:8000/diabetes-risk/ | SVM |
| 4 | Obesity Risk | http://127.0.0.1:8000/obesity/ | XGBoost |
| 5 | Segmentation | http://127.0.0.1:8000/segment/ | SVM |
| 6 | Limited Access | http://127.0.0.1:8000/access/ | KNN |
| 7 | Health Score | http://127.0.0.1:8000/predictor/ | Random Forest |
| 8 | Store Impact | http://127.0.0.1:8000/predictor/store/ | KNN |

---

## 🔧 Common Commands

### Start the Server
```bash
python manage.py runserver
```

### Start on a Different Port
```bash
python manage.py runserver 8080
```

### Make Migrations (if models change)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Admin User
```bash
python manage.py createsuperuser
```

### Check for Issues
```bash
python manage.py check
```

---

## 🔄 Git Commands

### Pull Latest Changes
```bash
git pull origin main
```

### Check Current Branch
```bash
git branch
```

### Switch to Main Branch
```bash
git checkout main
```

### View All Branches
```bash
git branch -a
```

### Create a New Branch
```bash
git checkout -b my-feature-branch
```

### Commit Changes
```bash
git add .
git commit -m "Your commit message"
git push origin your-branch-name
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution:** Install Django
```bash
pip install django
```

### Issue: "ModuleNotFoundError: No module named 'sklearn'"
**Solution:** Install scikit-learn
```bash
pip install scikit-learn
```

### Issue: "ModuleNotFoundError: No module named 'xgboost'"
**Solution:** Install XGBoost
```bash
pip install xgboost
```

### Issue: Port 8000 already in use
**Solution:** Use a different port
```bash
python manage.py runserver 8080
```

### Issue: "InconsistentVersionWarning" when loading models
**Note:** This is just a warning, not an error. The models will still work. To fix:
```bash
pip install scikit-learn==1.6.1
```

### Issue: Static files not loading (CSS broken)
**Solution:** Check that DEBUG=True in settings.py for development

---

## 📊 Testing the Models

Refer to `TESTING_GUIDE.md` for test values for each model.

### Quick Test Steps:
1. Start the server: `python manage.py runserver`
2. Open a model page (e.g., http://127.0.0.1:8000/quality/)
3. Enter test values from the testing guide
4. Click the submit/predict button
5. Verify the prediction matches expected results

---

## 👥 Team Branches

| Branch | Owner | Models |
|--------|-------|--------|
| main | Meriem | obj1, obj2, diabetes_risk |
| sarra | Sarra | segment, predictor (RF) |
| yomna | Yomna | obesity_predictor, Store Impact |
| ayoub | Ayoub | mlapp (Limited Access KNN) |

---

## 📞 Need Help?

If you encounter any issues:
1. Check the Troubleshooting section above
2. Make sure all dependencies are installed
3. Try deleting `__pycache__` folders and restarting
4. Contact the team lead

---

## 🎨 UI Theme

The application uses a premium dark theme with:
- Dark background (#0f172a)
- Teal/Cyan accent colors (#06b6d4)
- Glassmorphism effects
- Modern Inter font family

---

*Last Updated: January 3, 2026*
