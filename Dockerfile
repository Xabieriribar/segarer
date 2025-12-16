FROM python:3.12-slim

WORKDIR /app

# System deps for psycopg (binary usually enough, keep lean)
RUN pip install --no-cache-dir --upgrade pip

# Copy only dependency metadata first for caching
COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy the rest
COPY . /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
