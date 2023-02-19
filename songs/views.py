from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from . import models, serializers, services


class ArtistViewSet(ModelViewSet):
    queryset = models.Artist.objects.all()
    serializer_class = serializers.ArtistSerializer
    http_method_names = ["get", "post", "put", "delete"]


class AlbumViewSet(ModelViewSet):
    queryset = models.Album.objects.all()
    serializer_class = serializers.AlbumSerializer
    http_method_names = ["get", "post", "put", "delete"]

    @swagger_auto_schema(responses={200: serializers.AlbumRetrieveSerializer()})
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.AlbumRetrieveSerializer(instance=instance)
        return Response(serializer.data)


class AddSongToAlbumView(APIView):
    @swagger_auto_schema(
        request_body=serializers.AddSongToAlbumSerializer,
        responses={200: serializers.AlbumRetrieveSerializer()}
    )
    def post(self, request, *args, **kwargs):
        album = services.add_song_to_album(data=request.data.copy())
        serializer = serializers.AlbumRetrieveSerializer(instance=album)
        return Response(serializer.data)


class CreateSongView(APIView):
    @swagger_auto_schema(
        request_body=serializers.CreateSongSerializer,
        responses={200: serializers.SongCreateRetrieve()}
    )
    def post(self, request, *args, **kwargs):
        song = services.create_song(data=request.data.copy())
        serializer = serializers.SongCreateRetrieve(instance=song)
        return Response(serializer.data)


class RemoveSongFromAlbumView(APIView):
    @swagger_auto_schema(
        request_body=serializers.SongRemoveFromAlbum,
        responses={200: serializers.AlbumRetrieveSerializer()}
    )
    def delete(self, request, *args, **kwargs):
        services.remove_song_from_album(data=request.data.copy())
        return Response(status=204)


class SongViewSet(ModelViewSet):
    queryset = models.Song.objects.all()
    serializer_class = serializers.ArtistSerializer
    http_method_names = ["get", "put", "delete"]
