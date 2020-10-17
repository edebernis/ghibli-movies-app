#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pytest import fixture


@fixture
def app():
    from ghibli.app import create_app

    return create_app()


@fixture
def api(requests_mock):
    from ghibli.app import create_api

    api = create_api()

    requests_mock.get(
        'https://ghibliapi.herokuapp.com/films',
        text=open('tests/mocks/films.json').read()
    )
    requests_mock.get(
        'https://ghibliapi.herokuapp.com/people',
        text=open('tests/mocks/people.json').read()
    )

    return api
