from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from typing import Optional

# Load model
model = joblib.load(r"model_pipeline.pkl")

# Initialize FastAPI
app = FastAPI()

# Define request structure
class ReviewInput(BaseModel):
    reviewID: Optional[int] = 1
    verified: bool
    reviewTime: Optional[str] = None
    reviewerID: str
    asin: str
    reviewerName: Optional[str] = None
    reviewText: str
    summary: str
    unixReviewTime: Optional[str] = None
    overall: float

@app.post("/predict")
def predict(review: ReviewInput):
    try:
        # Combine text fields
        text = (review.reviewText or "") + " " + (review.summary or "")
        len_review = len(review.reviewText or "")
        len_summary = len(review.summary or "")
        len_text = len(text)

        # Safe datetime parsing
        days = 0
        if review.reviewTime:
            try:
                review_dt = pd.to_datetime(review.reviewTime, errors="coerce")
                if pd.notnull(review_dt):
                    days = (pd.Timestamp.today() - review_dt).days
            except Exception as e:
                print("Error parsing reviewTime:", e)
                days = 0

        # Create input DataFrame
        data = pd.DataFrame([{
            "asin": review.asin,
            "reviewerID": review.reviewerID,
            "overall": review.overall,
            "verified": int(review.verified),
            "days": days,
            "len_review": len_review,
            "len_summary": len_summary,
            "len_text": len_text,
            "clean_text": text
        }])

        # Predict
        pred = model.predict(data)[0]
        proba = model.predict_proba(data)[0][1]

        return {"prediction": int(pred), "probability": round(proba, 4)}
    
    except Exception as e:
        print("Unhandled exception:", e)
        return {"error": "Internal Server Error", "details": str(e)}