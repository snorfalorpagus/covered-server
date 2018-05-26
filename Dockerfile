FROM python:stretch

LABEL maintainer "Joshua Arnott <josh@snorfalorpagus.net>"

RUN apt-get update && apt-get upgrade -y

RUN pip install pipenv

COPY . /app

WORKDIR /app

RUN pipenv install --system --deploy

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi"]
