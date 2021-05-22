FROM python:3.8.5-slim
RUN apt-get update && apt-get install -y gcc=4:8.3.0-1 libpq-dev && rm -rf /var/lib/apt/lists/*
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /logs/django
RUN python manage.py collectstatic --no-input
CMD ["python","manage.py","runserver"]
