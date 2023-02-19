from rest_framework import serializers

from . import models


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artist
        fields = ["name"]


class AlbumSerializer(serializers.ModelSerializer):
    artist = serializers.CharField(source="artist.name")
    release_year = serializers.IntegerField(min_value=1900)

    class Meta:
        model = models.Album
        fields = ["id", "artist", "release_year"]


class AlbumSongSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="song.title")

    class Meta:
        model = models.AlbumSong
        fields = ["id", "order_number", "title"]


class BaseSong(serializers.Serializer):
    order_number = serializers.IntegerField(min_value=1)
    album = serializers.IntegerField(min_value=1)


class AddSongToAlbumSerializer(BaseSong):
    song = serializers.IntegerField(min_value=1)


class CreateSongSerializer(BaseSong):
    title = serializers.CharField(max_length=255)


class SongCreateRetrieve(serializers.ModelSerializer):
    title = serializers.CharField(source="song.title")
    order_number = serializers.IntegerField(min_value=1)
    album = serializers.CharField(source="album.pk")

    class Meta:
        model = models.AlbumSong
        fields = ["id", "order_number", "title", "album"]


class SongRemoveFromAlbum(serializers.Serializer):
    album = serializers.IntegerField(min_value=1)
    song = serializers.IntegerField(min_value=1)


class AlbumRetrieveSerializer(serializers.ModelSerializer):
    release_year = serializers.IntegerField(min_value=1900)
    songs = AlbumSongSerializer(many=True, read_only=True)

    class Meta:
        model = models.Album
        fields = ["id", "artist", "release_year", "songs"]
