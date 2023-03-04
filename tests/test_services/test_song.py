import pytest
from django.http import Http404

from songs.services import get_song
from songs.models import Song


class TestGetSong:
    def test_successful(self, song: Song):
        song_in_db = get_song(id_=song.id)
        assert song == song_in_db

    def test_successful_multiple_exist(self, songs: [Song]):
        song = songs[0]
        song_in_db = get_song(id_=song.id)
        assert song == song_in_db

    def test_not_exists(self, songs: [Song]):
        with pytest.raises(Http404) as exc:
            get_song(id_=1000)
        assert isinstance(exc.value, Http404)
