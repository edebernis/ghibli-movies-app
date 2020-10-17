#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pytest import fixture


@fixture
def api(requests_mock):
    requests_mock.get(
        'https://ghibliapi.herokuapp.com/films',
        text=open('tests/mocks/films.json').read()
    )
    requests_mock.get(
        'https://ghibliapi.herokuapp.com/people',
        text=open('tests/mocks/people.json').read()
    )

    from ghibli.app import api, stop_background_thread

    stop_background_thread()
    return api


@fixture
def app():
    from ghibli.app import app, stop_background_thread

    stop_background_thread()
    return app
