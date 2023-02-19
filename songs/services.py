from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound

from . import models, serializers


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
        models.AlbumSong.objects.create(
            order_number=serializer.validated_data["order_number"],
            song=song,
            album=album
        )
        album.refresh_from_db()
        return album


def create_song(data: dict) -> models.AlbumSong:
    serializer = serializers.CreateSongSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        album = get_album(id_=data["album"])
        try:
            with transaction.atomic():
                song = models.Song.objects.create(title=serializer.validated_data["title"])
                album_song = models.AlbumSong.objects.create(
                    order_number=serializer.validated_data["order_number"],
                    song=song,
                    album=album
                )
            return album_song
        except IntegrityError as exc:
            #TODO: implement except
            pass


def remove_song_from_album(data: dict) -> models.Album:
    album = get_album(id_=data["album"])
    song = album.songs.filter(pk=data["song"])
    if not song:
        raise NotFound()
    song.delete()
    album.refresh_from_db()
    return album
