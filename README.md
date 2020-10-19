# ghibli-movies-app
uWSGI Python web application, compatible Python 3.8+, that list movies produced by Ghibli studios.

## Description

Studio Ghibli is a Japanese movie company. This application relies on their REST API to provide information about movies and people (characters).

## Architecture

Ghibli application is a Python web application built using [Bottle web framework](https://bottlepy.org/docs/0.12/).

## Usage

Ghibli application is containerized with [Docker](https://www.docker.com/). You can simply run Ghibli app using [Docker Compose](https://docs.docker.com/compose/):

```bash
$ docker-compose up
```

## Environment variables

Following environment variables are configurable:
* GHIBLI_API_URL: URL of Ghibli REST API
* TEMPLATES_DIR: Path to HTML templates directory
* UPDATES_INTERVAL: Interval in seconds between data updates
* DEBUG: Enable debug mode

## Tests

Ghibli app uses [Pytest](https://docs.pytest.org/en/latest/) and [Tox](https://tox.readthedocs.io/en/latest/) for unit testing. To run tests, type following command in project root directory:

```bash
$ tox
```

Tests could be extended with integration testing, to make sure Ghibli REST API is still up and response formats do not change.
