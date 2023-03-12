from functools import partial

from django.urls import reverse
from rest_framework.test import APIClient

from songs.models import Album, Artist, Song
from songs.serializers import AlbumRetrieveSerializer, AlbumSerializer


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

    def test_artists_exist(self, api_client: APIClient, artists: [Artist], built_album_without_artist: Album):
        artist = artists[0]
        response = api_client.post(
            self.url,
            data={
                "release_year": built_album_without_artist.release_year,
                "artist": artist.id
            }
        )
        assert response.status_code == 201

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

    def test_none_artist_exist(self, api_client: APIClient, built_album_without_artist: Album):
        response = api_client.post(
            self.url,
            data={
                "release_year": built_album_without_artist.release_year,
                "artist": 1
            }
        )
        assert response.status_code == 400

    def test_with_invalid_field(self, api_client: APIClient, built_album: Album):
        response = api_client.post(
            self.url,
            data={
                "release_year": built_album.release_year,
                "artist": built_album.artist,
                "field": "stub"
            }
        )
        assert response.status_code == 400


class TestRetrieveAlbum:
    url = partial(reverse, "albums-detail")

    def test_successful(self, api_client: APIClient, album: Album):
        response = api_client.get(self.url(kwargs={"pk": album.id}))
        assert response.status_code == 200
        assert response.data == AlbumRetrieveSerializer(album).data

    def test_multiple_albums_exist(self, api_client: APIClient, albums: [Album]):
        response = api_client.get(self.url(kwargs={"pk": albums[1].id}))
        assert response.status_code
        assert response.data == AlbumRetrieveSerializer(albums[1]).data

    def test_none_exist(self, db, api_client: APIClient):
        response = api_client.get(self.url(kwargs={"pk": 1}))
        assert response.status_code == 404

    def test_not_exists_album(self, api_client: APIClient, albums: [Album]):
        response = api_client.get(self.url(kwargs={"pk": 1000}))
        assert response.status_code == 404


class TestListAlbum:
    url = reverse("albums-list")

    def test_successful(self, api_client: APIClient, albums: [Album]):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert response.data == AlbumSerializer(many=True, instance=albums).data

    def test_none_exist(self, db, api_client: APIClient):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert not response.data

    def test_one_exists(self, api_client: APIClient, album: Album):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert dict(response.data[0]) == AlbumSerializer(instance=album).data

    def test_with_songs(self, api_client: APIClient, albums_with_songs: dict):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert response.data == AlbumSerializer(many=True, instance=albums_with_songs["albums"]).data

    def test_one_with_songs(self, api_client: APIClient, album_with_songs: dict):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert dict(response.data[0]) == AlbumSerializer(instance=album_with_songs["album"]).data


class TestUpdateAlbum:
    url = partial(reverse, "albums-detail")
    release_year = 2019
    not_year = "not valid year"

    def test_successful(self, api_client: APIClient, album: Album):
        album.release_year = self.release_year
        response = api_client.patch(self.url(kwargs={"pk": album.id}), data={"release_year": self.release_year})
        assert response.status_code == 200
        assert response.data == AlbumSerializer(instance=album).data

    def test_multiple_exist_successful(self, api_client: APIClient, albums: [Album]):
        album = albums[0]
        album.release_year = self.release_year
        response = api_client.patch(self.url(kwargs={"pk": album.id}), data={"release_year": self.release_year})
        assert response.status_code == 200
        assert response.data == AlbumSerializer(instance=album).data

    def test_with_invalid_data(self, api_client: APIClient, album: Album):
        response = api_client.patch(self.url(kwargs={"pk": album.id}), data={"release_year": self.not_year})
        assert response.status_code == 400

    def test_none_exist(self, db, api_client: APIClient):
        response = api_client.patch(self.url(kwargs={"pk": 1}), data={"release_year": self.release_year})
        assert response.status_code == 404

    def test_not_exists(self, api_client: APIClient, albums: [Album]):
        response = api_client.patch(self.url(kwargs={"pk": 1000}), data={"release_year": self.release_year})
        assert response.status_code == 404

    def test_not_exists_with_invalid_data(self, api_client: APIClient, albums: [Album]):
        response = api_client.patch(self.url(kwargs={"pk": 1000}), data={"release_year": self.not_year})
        assert response.status_code == 404


class TestDeleteAlbum:
    pass
