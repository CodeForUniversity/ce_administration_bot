FROM python:3.12-slim

LABEL authors="mahdiar"

WORKDIR /app

COPY requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
