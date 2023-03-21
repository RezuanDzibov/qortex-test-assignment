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
