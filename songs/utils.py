from datetime import date

from . import models


def get_next_order_number(album: models.Album) -> int:
    return album.songs.all().count() + 1


def get_current_year() -> int:
    return date.today().year
