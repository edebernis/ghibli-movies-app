#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pytest import mark
from webtest import TestApp

# Prevent pytest from trying to collect webtest's TestApp as tests:
TestApp.__test__ = False


@mark.usefixtures("app")
def test_get_movies(app):
    test_app = TestApp(app)
    response = test_app.get('/movies')

    assert response.status == '200 OK'
