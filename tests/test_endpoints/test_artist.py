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

    def test_with_invalid_data(self, db, api_client: APIClient):
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

    def test_none_exist(self, db, api_client: APIClient):
        response = api_client.get(self.url(kwargs={"pk": 1000}))
        assert response.status_code == 404

    def test_not_exists_artist(self, api_client: APIClient, artists: [Artist]):
        response = api_client.get(self.url(kwargs={"pk": 1000}))
        assert response.status_code == 404


class TestListArtist:
    url = reverse("artists-list")

    def test_successful(self, api_client: APIClient, artists: [Artist]):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert response.data == ArtistSerializer(many=True, instance=artists).data

    def test_none_exist(self, db, api_client: APIClient):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert not response.data


class TestUpdateArtist:
    url = partial(reverse, "artists-detail")

    def test_successful(self, api_client: APIClient, artist: Artist):
        name = "name"
        artist.name = name
        response = api_client.put(self.url(kwargs={"pk": artist.id}), data={"name": name})
        assert response.status_code == 200
        assert response.data == ArtistSerializer(instance=artist).data

    def test_multiple_exist_successful(self, api_client: APIClient, artists: [Artist]):
        artist = artists[0]
        name = "name"
        artist.name = name
        response = api_client.put(self.url(kwargs={"pk": artist.id}), data={"name": name})
        assert response.status_code == 200
        assert response.data == ArtistSerializer(instance=artist).data

    def test_with_invalid_data(self, api_client: APIClient, artist: Artist):
        response = api_client.put(self.url(kwargs={"pk": artist.id}), data={"name": "s" * 256})
        assert response.status_code == 400

    def test_not_found(self, db, api_client: APIClient):
        response = api_client.put(self.url(kwargs={"pk": 1}), data={"name": "name"})
        assert response.status_code == 404

    def test_not_found_exist(self, api_client: APIClient, artists: [Artist]):
        response = api_client.put(self.url(kwargs={"pk": 1000}), data={"name": "name"})
        assert response.status_code == 404

    def test_not_found_with_invalid_data(self, api_client: APIClient, artists: [Artist]):
        response = api_client.put(self.url(kwargs={"pk": 1000}), data={"name": "a" * 256})
        assert response.status_code == 404


class TestDeleteArtist:
    url = partial(reverse, "artists-detail")

    def test_successful(self, api_client: APIClient, artist: Artist):
        response = api_client.delete(self.url(kwargs={"pk": artist.id}))
        assert response.status_code == 204
        assert api_client.get(self.url(kwargs={"pk": artist.id})).status_code == 404

    def test_multiple_exist_successful(self, api_client: APIClient, artists: [Artist]):
        artist = artists[0]
        response = api_client.delete(self.url(kwargs={"pk": artist.id}))
        assert response.status_code == 204
        assert api_client.get(self.url(kwargs={"pk": artist.id})).status_code == 404

    def test_none_exist(self, db, api_client: APIClient):
        response = api_client.delete(self.url(kwargs={"pk": 1}))
        assert response.status_code == 404

    def test_not_exists(self, api_client: APIClient, artists: [Artist]):
        response = api_client.delete(self.url(kwargs={"pk": 1000}))
        assert response.status_code == 404
