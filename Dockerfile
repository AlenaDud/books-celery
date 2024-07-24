FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Additional dependencies
  && apt-get install -y git \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt /app/
COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000