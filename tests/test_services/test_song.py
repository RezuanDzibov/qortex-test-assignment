import pytest
from django.http import Http404

from songs.services import get_song
from songs.models import Song


class TestGetSong:
    def test_successful(self, song: Song):
        song_in_db = get_song(id_=song.id)
        assert song == song_in_db

