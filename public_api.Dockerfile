# Use official Python image
FROM python:3.13

# Set working directory
WORKDIR /app

# Install uv package manager globally
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies globally (no venv)
RUN uv pip install -r requirements.txt --system

# Expose port (optional)
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

