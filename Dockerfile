FROM python:3.12-slim
WORKDIR /code
COPY pyproject.toml ./
RUN pip install --no-cache-dir .
COPY app ./app
CMD ["sh", "-c", "python -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
