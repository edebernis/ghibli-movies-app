#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pytest import mark


@mark.usefixtures("api")
def test_get_movies(api):
    movies = api.get_movies()

    assert isinstance(movies, dict)
    assert len(movies) == 2
    assert len(
        movies.get('https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe')
        .get('people')
    ) == 2
    assert len(
        movies.get('https://ghibliapi.herokuapp.com/films/12cfb892-aac0-4c5b-94af-521852e46d6a')
        .get('people')
    ) == 0
