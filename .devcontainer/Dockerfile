FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Configure Poetry to not create virtual environments inside the project
RUN poetry config virtualenvs.in-project false

# Set working directory
WORKDIR /workspace

# Copy pyproject.toml
COPY pyproject.toml ./

# Generate poetry.lock and install dependencies
RUN poetry lock -vvv && poetry install -vvv --no-root

# Set Python path
ENV PYTHONPATH=/workspace
