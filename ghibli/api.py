#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


class GhibliAPI:
    def __init__(self, base_url):
        self._base_url = base_url

    @staticmethod
    def create(url):
        base_url = url.rstrip('/')

        return GhibliAPI(base_url)

    def _fetch(self, url, timeout=3):
        response = requests.get(
            '{}/{}'.format(self._base_url, url),
            timeout=timeout)

        response.raise_for_status()
        return response.json()

    def _fetch_movies(self):
        return self._fetch('films')

    def _fetch_people(self):
        return self._fetch('people')

    def get_movies(self):
        movies = self._fetch_movies()
        movies_dict = {}
        for movie in movies:
            movie['people'] = []
            movies_dict[movie.get('url')] = movie

        people = self._fetch_people()
        for actor in people:
            for film in actor.get('films'):
                movies_dict.get(film)['people'].append(actor)

        return movies_dict
