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

COPY ./.docker/backend/docker-entrypoint.sh /app
RUN chmod +x /app/docker-entrypoint.sh

# Create a non-root user
RUN useradd -ms /bin/bash backenduser

# Set the ownership of the application directory to the non-root user
RUN chown -R backenduser:backenduser /app

# Switch to the non-root user
USER backenduser

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]

