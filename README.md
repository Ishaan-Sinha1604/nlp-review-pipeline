# 🧠 NLP Review Pipeline: Predicting Review Helpfulness

This end‑to‑end project demonstrates how to build, containerize, test, and deploy an NLP‑powered ML model as a REST API using **FastAPI**, **Docker**, **GitHub Actions (CI/CD)**, and **Render**.

---

## 🚀 Live Demo

**Test the Web App on Swagger UI:**  
[https://nlp-review-pipeline.onrender.com/docs](https://nlp-review-pipeline.onrender.com/docs)

---

## 🎯 Project Overview

**Objective:**  
Predict whether an Amazon product review will be marked as *helpful* (`label = 1`) or *not helpful* (`label = 0`) based on its textual content and metadata.

**Dataset:**  
- **Source:** Amazon Product Reviews (1996–2018)  
- **Key Features:** review text, summary, overall rating, reviewer ID, ASIN, verified purchase flag, review timestamp  

**Why It Matters:**  
- **Business Insight:** Helps e‑commerce platforms surface the most useful reviews.  
- **User Experience:** Improves product browsing by prioritizing helpful feedback.

---

## 🧰 Tech Stack

| Layer           | Tool / Library                    |
|-----------------|-----------------------------------|
| **Data & NLP**  | Python, Pandas, NLTK, scikit‑learn |
| **API Layer**   | FastAPI, Pydantic, Uvicorn         |
| **Container**   | Docker                             |
| **CI/CD**       | GitHub Actions                     |
| **Deployment**  | Render                             |
| **Testing**     | Pytest, pytest‑cov                 |

---

## 🔍 Methodology

### 1. Data Preprocessing  
- **Deduplication:** Drop duplicate reviews by `reviewerID` & `asin`.  
- **Date Handling:** Convert `reviewTime` to datetime and compute days since review.  
- **Text Merge:** Combine `reviewText` + `summary` into a single field.  
- **Feature Engineering:**  
  - Text features - Tokenization, Lemmatiation, Stop Words Removal
                  - TF‑IDF (unigrams & bigrams, max 5 k features)  
  - Numeric features: review length, summary length, days since review  
  - Categorical: one‑hot encode `overall`, `verified`, `asin`, `reviewerID`

### 2. Modeling  
- **Algorithm:** Logistic Regression (max_iter=500)  
- **Train/Test Split:** 80% train / 20% test, stratified on `label`  
- **Evaluation:** Classification report, ROC AUC, confusion matrix  

### 3. Deployment Pipeline  
1. **API:** Wrap the trained `model_pipeline.pkl` with FastAPI (`GET /` health check, `POST /predict`)  
2. **Containerization:** Dockerfile builds a stable Python environment, installs dependencies, exposes port 8000, runs Uvicorn  
3. **CI:** GitHub Actions runs on every push/PR — installs deps, sets `PYTHONPATH`, lints, runs Pytest with coverage  
4. **CD:** On `master` push, Actions builds the Docker image and triggers a Render deploy hook (cloud depoyment) 

---

---

## 📁 Project Structure

```

├── app/
│   ├── app.py            # FastAPI routes & model loader
│   ├── model_pipeline.pkl
│   └── requirements.txt
├── tests/
│   └── test_app.py       # Unit tests for / and /predict
├── .github/
│   └── workflows/
│       ├── ci.yml        # CI pipeline (tests, lint, coverage)
│       └── cd.yml        # CD pipeline (build & deploy)
├── Dockerfile
└── README.md

```

---

## ⚙️ Quickstart

### 1. Clone the repo
```
git clone https://github.com/Ishaan-Sinha1604/nlp-review-pipeline.git
cd nlp-review-pipeline
```
### 2. Local Docker Build & Run
```
docker build -t nlp-review-pipeline .
docker run -p 8000:8000 nlp-review-pipeline
```
Navigate to http://localhost:8000/docs

### 3. Or run locally without Docker
```
python -m venv venv
source venv/bin/activate      # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.app:app --reload
```

### 4. Testing
```
pytest --cov=app --cov-report=term-missing
```

---

## 💬 Example Request

```
{
  "reviewID": 1,
  "verified": true,
  "reviewerID": "string",
  "asin": "string",
  "reviewerName": "string",
  "reviewText": "string",
  "summary": "string",
  "unixReviewTime": "string",
  "overall": 0
}
```

---

## 🏗️ CI/CD Badges

![CI](https://github.com/Ishaan-Sinha1604/nlp-review-pipeline/actions/workflows/ci_cd.yml/badge.svg)
![CD](https://github.com/Ishaan-Sinha1604/nlp-review-pipeline/actions/workflows/deploy.yml/badge.svg)

---

## 📈 Future Enhancements
- Streamlit or simple React frontend
- /metrics endpoint for basic observability
- MLflow experiment tracking
- Logging & monitoring integration

---

## 📬 Contact

**Ishaan Sinha**  
📫 [ishaan.sinha1997@gmail.com](mailto:ishaan.sinha1997@gmail.com)  
🔗 [LinkedIn](https://ca.linkedin.com/in/ishaan-sinha-56a968167)

---

## 📄 License

MIT © Ishaan Sinha
This project is licensed under the [MIT License](./LICENSE).  
You are free to use, modify, and distribute this software with attribution.

---
