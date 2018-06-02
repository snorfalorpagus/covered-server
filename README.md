# covered-server

Server application for the *covered* coverage tool.

The application is still in development and as such the API is not stable.

## Running the application

### Development mode

To start the server in development mode:

```
$ export PYTHONPATH=.
$ export FLASK_APP=app.wsgi
$ export FLASK_ENV=development
$ flask run
* Serving Flask app "app.wsgi"
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Gunicorn

To start the server with gunicorn (recommended for production)

```
$ gunicorn --bind 0.0.0.0:8000 app.wsgi
[2018-06-02 11:04:46 +0000] [1] [INFO] Starting gunicorn 19.8.1
[2018-06-02 11:04:46 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
[2018-06-02 11:04:46 +0000] [1] [INFO] Using worker: sync
[2018-06-02 11:04:46 +0000] [9] [INFO] Booting worker with pid: 9
```

### Docker container

To build the Docker image:

```
$ docker build -t covered-server .
```

To start a Docker container:

```
$ docker run -p 8000:8000 -it covered-server
```

## Tests

### Locally

```
$ python -m pytest tests --cov=app
```

### Drone CI

```
$ drone exec
```
