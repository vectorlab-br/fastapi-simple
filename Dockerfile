FROM python:3.10-slim

RUN useradd -ms /bin/bash appuser

WORKDIR /app

# Avoid the .pyc generation
ENV PYTHONDONTWRITEBYTECODE=1

# Turn off buffering for easy container logging
ENV PYTHONUNBUFFERED=1

ENV USE_HTTPS=0

COPY requirements.txt .
# RUN mkdir db
# COPY ./db/nomes_cemiterios.txt db/
# COPY ./db/nomes_pessoas.txt db/
RUN python -m pip install --upgrade pip \
&& pip install --no-cache-dir -r requirements.txt

COPY src/main.py .
COPY templates ./templates
COPY static ./static
COPY db ./db

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--proxy-headers", "--forwarded-allow-ips=*"]