from django.urls import reverse
from rest_framework.test import APIClient

from songs.models import Song


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
