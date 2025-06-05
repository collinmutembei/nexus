# --- Base image with Python 3.12 ---
FROM python:3.12-slim AS base

# Install uv (universal virtualenv)
RUN pip install --no-cache-dir uv

# Set work directory
WORKDIR /app

# Copy only dependency files for layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv pip install --system --no-cache-dir -r pyproject.toml

# --- Builder stage (optional, for collecting static files, compiling, etc.) ---
FROM base AS builder

# Copy the rest of the application code
COPY . .

# --- Final image ---
FROM python:3.12-slim AS final

WORKDIR /app

# Copy installed dependencies from base image
COPY --from=base /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=base /usr/local/bin /usr/local/bin
COPY --from=base /usr/local/include /usr/local/include

# Copy application code from builder
COPY --from=builder /app .

# Expose port (if needed)
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command (adjust as needed)
CMD ["gunicorn", "nexus.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
