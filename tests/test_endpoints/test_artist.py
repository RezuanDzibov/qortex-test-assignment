from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from songs.models import Artist


class TestCreateArtist:
    url = reverse("artists-list")

    def test_successful(self, db, api_client: APIClient, built_artist: Artist):
        response = api_client.post(self.url, data={"name": built_artist.name})
        assert response.status_code == 201

    def test_invalid_data(self, db, api_client: APIClient):
        response = api_client.post(self.url, data={"name": "a" * 256})
        assert response.status_code == 400


class TestRetrieveArtist:
    def test_successful(self, api_client: APIClient, artist: Artist):
        response = api_client.get(reverse("artists-detail", kwargs={"pk": artist.id}))
        assert response.status_code == 200
        assert response.data["id"] == artist.id

    def test_multiple_artists_exist(self, api_client: APIClient, artists: [Artist]):
        response = api_client.get(reverse("artists-detail", kwargs={"pk": artists[1].id}))
        assert response.status_code
        assert response.data["id"] == artists[1].id

    def test_not_found(self, db, api_client: APIClient):
        response = api_client.get(reverse("artists-detail", kwargs={"pk": 1000}))
        assert response.status_code == 404

    def test_not_exists_artist(self, api_client: APIClient, artists: [Artist]):
        response = api_client.get(reverse("artists-detail", kwargs={"pk": 1000}))
        assert response.status_code == 404
