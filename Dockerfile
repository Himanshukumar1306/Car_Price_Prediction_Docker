# Use a lightweight, official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy requirements file first to utilize Docker layer cache
COPY requirements.txt .

# Install dependencies securely and cleanly
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy only the necessary files for running the web server and inference
COPY app.py .
COPY model.pkl .
COPY templates/ ./templates/

# Create a non-privileged system user and group to run the app securely (not as root)
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -s /sbin/nologin appuser && \
    chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose port 5000 (documentation purpose; overridden by Render routing)
EXPOSE 5000

# Health check using Python's built-in urllib reading the dynamic port environment variable (defaulting to 5000)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request, os; port=os.environ.get('PORT', '5000'); urllib.request.urlopen(f'http://localhost:{port}/health')" || exit 1

# Start the Flask app using Gunicorn binding to the dynamic $PORT (defaulting to 5000 via env shell evaluation)
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 app:app
