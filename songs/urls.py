from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("artists", views.ArtistViewSet, basename="artists")
router.register("albums", views.AlbumViewSet, basename="albums")
router.register("songs", views.SongViewSet, basename="songs")

urlpatterns = [
    path("albums/add_song/", views.AddSongToAlbumView.as_view(), name="add_song_to_album"),
    path("albums/remove_song/", views.RemoveSongFromAlbumView.as_view(), name="remove_song_from_album"),
    path("songs/", views.CreateSongView.as_view(), name="create_song"),
]

urlpatterns += router.urls
