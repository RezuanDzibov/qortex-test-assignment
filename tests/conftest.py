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

