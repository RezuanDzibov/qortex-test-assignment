from . import models


def get_next_order_number(album: models.Album) -> int:
    return album.songs.all().count() + 1
