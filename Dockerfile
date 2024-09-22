FROM python:3.10-slim

WORKDIR /app

# Avoid the .pyc generation
ENV PYTHONDONTWRITEBYTECODE=1

# Turn off buffering for easy container logging
ENV PYTHONUNBUFFERED=1

ENV USE_HTTPS=0

COPY requirements.txt .
COPY nomes_cemiterios.txt .
COPY nomes_pessoas.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py .
COPY templates ./templates
COPY static ./static

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--proxy-headers", "--forwarded-allow-ips=*"]