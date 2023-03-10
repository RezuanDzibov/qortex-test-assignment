from rest_framework import serializers

from . import models
from .utils import get_current_year


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artist
        fields = ["id", "name"]


class AddSongToAlbumSerializer(serializers.Serializer):
    song = serializers.IntegerField(min_value=1)


class AlbumSerializer(serializers.ModelSerializer):
    release_year = serializers.IntegerField(min_value=1900, default=get_current_year, required=False)

    class Meta:
        model = models.Album
        fields = ["id", "artist", "release_year"]


class AlbumSongSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="song.id")
    title = serializers.CharField(source="song.title")

    class Meta:
        model = models.AlbumSong
        fields = ["id", "order_number", "title"]


class AlbumRetrieveSerializer(serializers.ModelSerializer):
    release_year = serializers.IntegerField(min_value=1900)
    songs = AlbumSongSerializer(many=True, read_only=True)

    class Meta:
        model = models.Album
        fields = ["id", "artist", "release_year", "songs"]


class SongCreateRetrieveSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="song.title")
    album = serializers.CharField(source="album.pk")
    order_number = serializers.IntegerField(min_value=1)

    class Meta:
        model = models.AlbumSong
        fields = ["id", "order_number", "title", "album"]


class SongRemoveFromAlbumSerializer(serializers.Serializer):
    song = serializers.IntegerField(min_value=1)


class SongRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Song
        fields = ["id", "title"]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "title": instance.title,
            "in_albums": [album_song.album.id for album_song in instance.album_songs.all()]
        }


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Song
        fields = ["id", "title"]
