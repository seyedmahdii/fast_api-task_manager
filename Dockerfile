FROM python:3.11-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy requirements first (for better caching)
COPY requirements.txt .

# 4. Install Python dependencies (During build)
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# 7. Command to run when container starts
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]
