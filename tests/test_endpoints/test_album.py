from django.urls import reverse
from rest_framework.test import APIClient

from songs.models import Album, Artist


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

    def test_with_invalid_data(self, api_client: APIClient, built_album: Album):
        built_album.release_year = "invalid_year"
        response = api_client.post(
            self.url,
            data={
                "release_year": built_album.release_year,
                "artist": built_album.artist.id
            }
        )
        assert response.status_code == 400

    def test_without_artist(self, api_client: APIClient, built_album_without_artist: Album):
        response = api_client.post(self.url, data={"release_year": built_album_without_artist.release_year})
        assert response.status_code == 400

    def test_not_exists_artist(self, api_client: APIClient, artist: Artist, built_album_without_artist: Album):
        response = api_client.post(
            self.url,
            data={
                "release_year": built_album_without_artist.release_year,
                "artist": 100
            }
        )
        assert response.status_code == 400
