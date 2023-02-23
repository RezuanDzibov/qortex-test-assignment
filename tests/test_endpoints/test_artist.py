from functools import partial

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from songs.models import Artist
from songs.serializers import ArtistSerializer


class TestCreateArtist:
    url = reverse("artists-list")

    def test_successful(self, db, api_client: APIClient, built_artist: Artist):
        response = api_client.post(self.url, data={"name": built_artist.name})
        assert response.status_code == 201
        assert response.data["name"] == built_artist.name

    def test_invalid_data(self, db, api_client: APIClient):
        response = api_client.post(self.url, data={"name": "a" * 256})
        assert response.status_code == 400


class TestRetrieveArtist:
    url = partial(reverse, "artists-detail")

    def test_successful(self, api_client: APIClient, artist: Artist):
        response = api_client.get(self.url(kwargs={"pk": artist.id}))
        assert response.status_code == 200
        assert response.data == ArtistSerializer(artist).data

    def test_multiple_artists_exist(self, api_client: APIClient, artists: [Artist]):
        response = api_client.get(self.url(kwargs={"pk": artists[1].id}))
        assert response.status_code
        assert response.data == ArtistSerializer(artists[1]).data

    def test_not_found(self, db, api_client: APIClient):
        response = api_client.get(self.url(kwargs={"pk": 1000}))
        assert response.status_code == 404

    def test_not_exists_artist(self, api_client: APIClient, artists: [Artist]):
        response = api_client.get(self.url(kwargs={"pk": 1000}))
        assert response.status_code == 404
