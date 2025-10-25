FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4321

ENTRYPOINT ["uvicorn", "main:app", "--env-file", ".env", "--host", "0.0.0.0", "--port", "4321"]