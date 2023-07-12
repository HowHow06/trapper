# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get install -y libmariadb3 libmariadb-dev
# the last line is to fix dependencies error when using mariadb connector

# Install dependencies
COPY ./backend/pyproject.toml ./backend/poetry.lock* /app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy the application code
COPY ./backend /app

ENV PYTHONPATH=/app


# Create a non-root user
RUN useradd -ms /bin/bash backenduser

# Set the ownership of the application directory to the non-root user
RUN chown -R backenduser:backenduser /app

# Switch to the non-root user
USER backenduser

EXPOSE 8000
# # Run the backend with gunicorn
CMD ["poetry", "run", "gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "-b", "0.0.0.0:8000"]


# # Run the backend with uvicorn
# CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
