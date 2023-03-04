import pytest
from django.http import Http404
from rest_framework.exceptions import NotFound

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

    def test_none_exist_album(self, song: Song):
        with pytest.raises(Http404) as exc:
            services.add_song_to_album(data={"album": 1, "song": song.id})
        assert isinstance(exc.value, Http404)

    def test_not_exists_album(self, albums: Album, song: Song):
        with pytest.raises(Http404) as exc:
            services.add_song_to_album(data={"album": 1000, "song": song.id})
        assert isinstance(exc.value, Http404)

    def test_none_exist_song(self, album: Album):
        with pytest.raises(Http404) as exc:
            services.add_song_to_album(data={"album": album.id, "song": 1})
        assert isinstance(exc.value, Http404)

    def test_not_exists_song(self, album: Album, songs: [Song]):
        with pytest.raises(Http404) as exc:
            services.add_song_to_album(data={"album": album.id, "song": 1000})
        assert isinstance(exc.value, Http404)

    def test_add_to_albums(self, albums: [Album], song: Song):
        for album in albums:
            services.add_song_to_album(data={"album": album.id, "song": song.id})
        assert [album.id for album in albums] == [album_song.album.id for album_song in song.album_songs.all()]

    def test_add_multiple_songs_to_album(self, album: Album, songs: [Song]):
        for song in songs:
            services.add_song_to_album(data={"album": album.id, "song": song.id})
        assert [album_song.song.id for album_song in album.songs.all()] == [song.id for song in songs]

    @pytest.mark.parametrize("albums", [2], indirect=True)
    @pytest.mark.parametrize("songs", [2], indirect=True)
    def test_add_songs_to_albums(self, albums: [Album], songs: [Song]):
        for album, song in zip(albums, songs):
            services.add_song_to_album(data={"album": album.id, "song": song.id})
        assert songs[0].album_songs.filter(album=albums[0])
        assert songs[1].album_songs.filter(album=albums[1])


class TestRemoveSongFromAlbum:
    def test_successful(self, album_with_song: [Album, Song]):
        album = services.remove_song_from_album(data={"album": album_with_song[0].id, "song": album_with_song[1].id})
        assert not album.songs.filter(pk=album_with_song[1].id)

    def test_not_exits_album(self, song: Song):
        with pytest.raises(Http404) as exc:
            services.remove_song_from_album(data={"album": 1, song: song.id})
        assert isinstance(exc.value, Http404)

    def test_not_exists_song(self, album: Album):
        with pytest.raises(NotFound) as exc:
            services.remove_song_from_album(data={"album": album.id, "song": 1})
        assert exc.value.status_code == 404

    def test_album_with_many_songs(self, album_with_songs: dict):
        song = album_with_songs["songs"][0]
        album = services.remove_song_from_album(data={"album": album_with_songs["album"].id, "song": song.id})
        assert not album.songs.filter(song__pk=song.id)

    def test_albums_with_many_songs(self, albums_with_songs: dict):
        album = albums_with_songs["albums"][0]
        song = albums_with_songs["songs"][1]
        album = services.remove_song_from_album(data={"album": album.id, "song": song.id})
        assert not album.songs.filter(song__pk=song.id)
