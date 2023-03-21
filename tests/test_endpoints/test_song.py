from functools import partial

from django.urls import reverse
from rest_framework.test import APIClient

from songs.models import Song
from songs.serializers import SongRetrieveSerializer, SongSerializer


class TestCreateSong:
    url = reverse("songs-list")

    def test_create_one(self, db, api_client: APIClient, built_song: Song):
        data = {"title": built_song.title}
        response = api_client.post(self.url, data)
        response_data = response.data.copy()
        response_data.pop("id")
        assert response.status_code == 201
        assert response_data == data

    def test_with_invalid_data(self, db, api_client: APIClient):
        response = api_client.post(self.url, data={"title": "a" * 256})
        assert response.status_code == 400

    def test_with_not_exists_field(self, db, api_client: APIClient):
        response = api_client.post(self.url, data={"field": "value"})
        assert response.status_code == 400


class TestRetrieveSong:
    url = partial(reverse, "songs-detail")

    def test_get_one(self, api_client: APIClient, song: Song):
        response = api_client.get(self.url(kwargs={"pk": song.id}))
        assert response.status_code == 200
        assert response.data == SongRetrieveSerializer(song).data

    def test_multiple_exist(self, api_client: APIClient, songs: [Song]):
        response = api_client.get(self.url(kwargs={"pk": songs[1].id}))
        assert response.status_code
        assert response.data == SongRetrieveSerializer(songs[1]).data

    def test_none_exist(self, db, api_client: APIClient):
        response = api_client.get(self.url(kwargs={"pk": 1000}))
        assert response.status_code == 404

    def test_not_exists(self, api_client: APIClient, songs: [Song]):
        response = api_client.get(self.url(kwargs={"pk": 1000}))
        assert response.status_code == 404


class TestListSong:
    url = reverse("songs-list")

    def test_multiple_exist(self, api_client: APIClient, songs: [Song]):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert response.data == SongSerializer(many=True, instance=songs).data

    def test_none_exist(self, db, api_client: APIClient):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert not response.data

    def test_one_exists(self, api_client: APIClient, song: Song):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert dict(response.data[0]) == SongSerializer(instance=song).data
