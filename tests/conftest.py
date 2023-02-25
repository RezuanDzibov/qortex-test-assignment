from functools import partial
from random import randint
from typing import List

import pytest
from rest_framework.test import APIClient

from . import factories
from songs import models


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="function")
def built_artist() -> models.Artist:
    return factories.ArtistFactory.build()


@pytest.fixture(scope="function")
def artist(db, built_artist: models.Artist) -> models.Artist:
    return factories.ArtistFactory.create()


@pytest.fixture(scope="function")
def artists(request, db) -> [models.Artist]:
    func = partial(factories.ArtistFactory.create_batch)
    if hasattr(request, "param") and request.param is int and request.param > 0:
        artists = func(request.param)
    else:
        artists = func(randint(1, 6))
    return artists


@pytest.fixture(scope="function")
def album(artist: models.Artist) -> models.Album:
    album = factories.AlbumFactory(artist=artist)
    return album
