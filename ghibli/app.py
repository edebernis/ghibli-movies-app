#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = "0.0.1"

from datetime import datetime
from threading import Timer, Lock
from bottle import Bottle, SimpleTemplate, request, response
import os
import sys
import json
import atexit
import logging

from ghibli.api import GhibliAPI


# Init global variables
db = {}
background_thread = None
lock = Lock()


def setup_logging():
    level = logging.DEBUG \
        if bool(os.environ.get('DEBUG', False)) else logging.INFO

    logging.basicConfig(
        stream=sys.stdout,
        format='{\
            "level": "%(levelname)s",\
            "date": "%(asctime)s",\
            "message": "%(message)s"}',
        datefmt='%Y-%m-%dT%H:%M:%S%z',
        level=level)


def create_api():
    url = os.environ.get('GHIBLI_API_URL')
    if url is None:
        raise Exception('GHIBLI_API_URL environment variable is unset')

    return GhibliAPI.create(url)


def create_templates():
    templates_dirpath = os.environ.get('TEMPLATES_DIR', 'templates')
    if not os.path.exists(templates_dirpath):
        raise Exception('Templates directory "{}" does not exist'
              .format(templates_dirpath)
        )

    templates = {}
    for root, _, files in os.walk(templates_dirpath):
        for _file in files:
            name = os.path.splitext(_file)[0]
            templates[name] = SimpleTemplate(
                open(os.path.join(root, _file)).read()
            )

    return templates


def create_app():
    app = Bottle()

    def _error(code, err):
        response.content_type = 'application/json; charset=utf-8'
        return json.dumps({
            'code': code,
            'message': err.body
        })

    @app.hook('before_request')
    def _remove_trailing_slashes():
        request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')

    @app.error(code=400)
    def error400(err):
        return _error(400, err)

    @app.error(code=404)
    def error404(err):
        return _error(404, err)

    @app.error(code=500)
    def error500(err):
        logging.error(err.traceback)
        return _error(500, err)

    @app.get('/version')
    def get_version():
        return {'version': __version__}

    @app.get('/movies')
    def get_movies():
        global db
        global templates

        tpl = templates.get('movies')
        if tpl is None:
            raise Exception('No movies template loaded')

        return tpl.render(
            movies=db.get('movies'),
            updated_at=db.get('movies_updated_at')
        )

    return app


def update_movies():
    global db
    global api
    db['movies'] = api.get_movies()
    db['movies_updated_at'] = datetime.now()


def start_background_thread():
    try:
        movies_interval = int(os.environ.get('FETCH_MOVIES_INTERVAL', 60))
    except ValueError:
        raise Exception(
            'FETCH_MOVIES_INTERVAL environment variable must be an integer'
        )
    if movies_interval < 10:
        raise Exception(
            'FETCH_MOVIES_INTERVAL environment variable must be >= 15 seconds'
        )

    def run_background_task():
        with lock:
            update_movies()

        global background_thread
        background_thread = Timer(movies_interval, run_background_task)
        background_thread.start()

    run_background_task()
    atexit.register(stop_background_thread)


def stop_background_thread():
    global background_thread
    background_thread.cancel()


# Main
setup_logging()

api = create_api()
templates = create_templates()
app = application = create_app()

start_background_thread()
