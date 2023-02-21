from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from songs.models import Artist


class TestCreateArtist:
    def test_successful(self, db, api_client: APIClient, built_artist: Artist):
        response = api_client.post(reverse("artists-list"), data={"name": built_artist.name})
        assert response.status_code == 201
