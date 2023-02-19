from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound, APIException

from . import models, serializers
from .utils import get_next_order_number


def get_album(id_: int) -> models.Album:
    album = get_object_or_404(models.Album, pk=id_)
    return album


def get_song(id_: int) -> models.Song:
    song = get_object_or_404(models.Song, pk=id_)
    return song


def add_song_to_album(data: dict) -> models.Album:
    serializer = serializers.AddSongToAlbumSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        album = get_album(id_=data["album"])
        song = get_song(id_=serializer.validated_data["song"])
        if album.songs.filter(song=song):
            raise APIException(code=409, detail="Already exists")
        models.AlbumSong.objects.create(
            order_number=get_next_order_number(album=album),
            song=song,
            album=album
        )
        album.refresh_from_db()
        return album


def remove_song_from_album(data: dict) -> models.Album:
    album = get_album(id_=data["album"])
    song = album.songs.filter(pk=data["song"])
    if not song:
        raise NotFound()
    song.delete()
    album.refresh_from_db()
    return album
