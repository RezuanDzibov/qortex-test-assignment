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
    default_serializer_class = serializers.AlbumSerializer
    serializer_classes = {"create": serializers.AlbumCreateSerializer}
    http_method_names = ["get", "post", "put", "delete"]

    @swagger_auto_schema(responses={200: serializers.AlbumRetrieveSerializer()})
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.AlbumRetrieveSerializer(instance=instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


class AddSongToAlbumView(APIView):
    @swagger_auto_schema(
        request_body=serializers.AddSongToAlbumSerializer,
        responses={200: serializers.AlbumRetrieveSerializer()}
    )
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data["album"] = int(kwargs["pk"])
        album = services.add_song_to_album(data=data)
        serializer = serializers.AlbumRetrieveSerializer(instance=album)
        return Response(serializer.data)


class RemoveSongFromAlbumView(APIView):
    @swagger_auto_schema(
        request_body=serializers.SongRemoveFromAlbum,
        responses={204: ""}
    )
    def delete(self, request, *args, **kwargs):
        data = request.data.copy()
        data["album"] = kwargs["pk"]
        services.remove_song_from_album(data=data)
        return Response(status=204)


class SongViewSet(ModelViewSet):
    queryset = models.Song.objects.all()
    serializer_class = serializers.SongSerializer
    http_method_names = ["get", "put", "delete", "post"]

    @swagger_auto_schema(
        responses={200: serializers.SongRetrieveSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.SongRetrieveSerializer(instance=instance)
        return Response(serializer.data, status=200)
