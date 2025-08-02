# Use Official Python Image
FROM python:3.11-slim

# Set Environment Variables
ENV PYTHONWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

# Set Work Directory
WORKDIR /app

# Install Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project Files
COPY . .

# Expose Port
EXPOSE 8000

# Run The FastAPI Application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]