# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy app code and model
COPY ./app /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir fastapi uvicorn scikit-learn pandas joblib

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
