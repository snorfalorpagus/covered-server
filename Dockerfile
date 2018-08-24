FROM python:3.7-slim

LABEL maintainer "Joshua Arnott <josh@snorfalorpagus.net>"

WORKDIR /app
RUN pip install pipenv
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy
COPY . /app

USER www-data

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi"]
