# ghibli-movies-app
uWSGI web application that list movies produced by Ghibli studios, compatible Python 3.8+.

## Description

Studio Ghibli is a Japanese movie company. This application relies on their REST API to provide information about movies and people (characters).

## Architecture

Ghibli application is built using [Bottle web framework](https://bottlepy.org/docs/0.12/).

## Usage

Ghibli application is containerized with [Docker](https://www.docker.com/). You can simply run Ghibli app using [Docker Compose](https://docs.docker.com/compose/):

```bash
$ docker-compose up
```

## Environment variables

Following environment variables are configurable:
* GHIBLI_API_URL: URL to Ghibli REST API
* TEMPLATES_DIR: Path to templates directory
* UPDATES_INTERVAL: Interval between data updates
* DEBUG: Enable debug mode

## Tests

Ghibli app uses [Pytest](https://docs.pytest.org/en/latest/) and [Tox](https://tox.readthedocs.io/en/latest/) for unit testing. To run tests, type following command in project root directory:

```bash
$ tox
```
