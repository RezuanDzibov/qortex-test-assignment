import pytest
from django.http import Http404

from songs import services
from songs.models import Album, Song


class TestGetAlbum:
    def test_successful(self, album: Album):
        album_in_db = services.get_album(id_=album.id)
        assert album == album_in_db

    def test_successful_multiple_exist(self, albums: [Album]):
        album = albums[0]
        album_in_db = services.get_album(id_=album.id)
        assert album == album_in_db

    def test_not_exists(self, albums: [Album]):
        with pytest.raises(Http404) as exc:
            services.get_album(id_=1000)
        assert isinstance(exc.value, Http404)

    def test_none_exist(self, db):
        with pytest.raises(Http404) as exc:
            services.get_album(id_=1)
        assert isinstance(exc.value, Http404)


class TestAddSongToAlbum:
    def test_successful(self, album: Album, song: Song):
        album = services.add_song_to_album(data={"album": album.id, "song": song.id})
        assert album.songs.filter(pk=song.id)
