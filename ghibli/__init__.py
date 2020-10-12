#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = "0.0.1"

import os
import sys
import json
import logging
from bottle import Bottle, request, response, template

from ghibli.api import GhibliAPI


class GhibliApp(Bottle):
    __instance = None

    @staticmethod
    def get_instance():
        if GhibliApp.__instance is not None:
            return GhibliApp.__instance

        return GhibliApp.init()

    def __init__(self):
        super(GhibliApp, self).__init__()

        if GhibliApp.__instance is None:
            GhibliApp.__instance = self
        else:
            raise Exception('GhibliApp class is a singleton')

        self._api = None
        self._templates = None

    @staticmethod
    def init():
        app = GhibliApp()

        app.load_hooks()
        app.load_error_handlers()
        app.load_routes()
        app.load_api()
        app.load_templates()

        return app

    def load_api(self):
        self._api = GhibliAPI()

    def load_templates(self):
        templates_dirpath = os.environ.get('TEMPLATES_DIR', '')
        if not os.path.exists(templates_dirpath):
            raise Exception('Templates directory does not exist')

        self._templates = {}
        for root, _, files in os.walk(templates_dirpath):
            for _file in files:
                name = os.path.splitext(_file)[0]
                self._templates[name] = open(os.path.join(root, _file)).read()

    def load_hooks(self):
        @self.hook('before_request')
        def _remove_trailing_slashes():
            request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')

    def load_error_handlers(self):
        @self.error(code=400)
        def _error400(err):
            return self._error(400, err)

        @self.error(code=404)
        def _error404(err):
            return self._error(404, err)

        @self.error(code=500)
        def _error500(err):
            logging.error(err.traceback)
            return self._error(500, err)

    def load_routes(self):
        @self.get('/movies')
        def get_movies():
            movies = self._api.get_movies()
            return template(self._templates.get('movies'), movies=movies)

    def _error(self, code, err):
        response.content_type = 'application/json; charset=utf-8'
        return json.dumps({
            'code': code,
            'message': err.body
        })


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


def get_wsgi_application():
    setup_logging()

    app = GhibliApp.init()
    return app
