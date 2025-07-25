from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from typing import Optional
import os

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from prometheus_fastapi_instrumentator import Instrumentator

# Load model
model_path = os.path.join(os.path.dirname(__file__), "model_pipeline.pkl")
model = joblib.load(model_path)

# Initialize FastAPI
app = FastAPI()

# Instrumentation for Prometheus
# This will automatically expose metrics at /metrics endpoint
Instrumentator().instrument(app).expose(app)

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

# Root endpoint — useful for health check or info
@app.get("/")
def read_root():
    return {"message": "Welcome to the NLP Review Pipeline API!"}

# Predict endpoint
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
    
# Custom error handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        # Drop the 'input' field only for missing fields
        if err.get("type") == "missing":
            err.pop("input", None)
        errors.append(err)
    return JSONResponse(status_code=422, content={"detail": errors})


### Comment added for testing purposes