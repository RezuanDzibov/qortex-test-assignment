from songs import services
from songs.models import Album


class TestGetAlbum:
    def test_successful(self, album: Album):
        album_in_db = services.get_album(id_=album.id)
        assert album == album_in_db
