from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from songs.models import Artist


class TestCreateArtist:
    url = reverse("artists-list")

    def test_successful(self, db, api_client: APIClient, built_artist: Artist):
        response = api_client.post(self.url, data={"name": built_artist.name})
        assert response.status_code == 201
