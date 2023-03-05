from django.urls import reverse
from rest_framework.test import APIClient

from songs.models import Album


class TestCreateAlbum:
    url = reverse("albums-list")

    def test_successful(self, api_client: APIClient, built_album: Album):
        response = api_client.post(
            self.url,
            data={
                "release_year": built_album.release_year,
                "artist": built_album.artist.id
            }
        )
        assert response.status_code == 201
