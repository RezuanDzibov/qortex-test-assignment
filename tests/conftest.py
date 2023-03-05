from functools import partial
from random import randint

import pytest
from django.db import transaction
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
        artists = func(randint(2, 6))
    return artists


@pytest.fixture(scope="function")
def album(artist: models.Artist) -> models.Album:
    album = factories.AlbumFactory(artist=artist)
    return album


@pytest.fixture(scope="function")
def albums(request, artist: models.Artist) -> [models.Album]:
    func = partial(factories.AlbumFactory.create_batch, artist=artist)
    if hasattr(request, "param") and isinstance(request.param, int) and request.param:
        albums = func(request.param)
    else:
        albums = func(randint(2, 6))
    return albums


@pytest.fixture(scope="function")
def song(db) -> models.Song:
    song = factories.SongFactory.create()
    return song


@pytest.fixture(scope="function")
def songs(request, db) -> [models.Song]:
    func = partial(factories.SongFactory.create_batch)
    if hasattr(request, "param") and isinstance(request.param, int) and request.param > 0:
        songs = func(request.param)
    else:
        songs = func(randint(2, 6))
    return songs


@pytest.fixture(scope="function")
def album_with_song(album: models.Album, song: models.Song) -> [models.Album, models.Song]:
    models.AlbumSong.objects.create(
        song=song,
        album=album
    )
    return album, song


@pytest.fixture(scope="function")
def album_with_songs(album: models.Album, songs: [models.Song]) -> dict:
    album_songs = [models.AlbumSong(album=album, song=song) for song in songs]
    with transaction.atomic():
        for album_song in album_songs:
            album_song.save()
    return {"album": album, "songs": songs}


@pytest.fixture(scope="function")
def albums_with_songs(artist: models.Artist) -> dict:
    with transaction.atomic():
        songs = factories.SongFactory.create_batch(6)
        albums = factories.AlbumFactory.create_batch(artist=artist, size=2)
    _songs = {0: songs[0:3], 1: songs[3:]}
    for index, album in enumerate(albums):
        with transaction.atomic():
            for song in _songs[index]:
                factories.AlbumSongFactory.create(album=album, song=song)
    return {"albums": albums, "songs": songs}


@pytest.fixture(scope="function")
def built_album(artist) -> models.Album:
    return factories.AlbumFactory.build(artist=artist)


@pytest.fixture(scope="function")
def built_album_without_artist(db) -> models.Album:
    return factories.AlbumFactory.build()
