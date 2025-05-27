FROM python:3.10

WORKDIR /app

# Copy only requirements.txt first to cache
COPY requirements.txt .

# # Install dependency (will be cached if requirements.txt didn't change)
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# Prevent Docker from caching pip install
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
