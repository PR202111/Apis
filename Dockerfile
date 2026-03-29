FROM python:3.13.0

WORKDIR /usr/src/app

# Copy requirements first (for caching)
COPY requirements.txt ./

# Install dependencies correctly
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]