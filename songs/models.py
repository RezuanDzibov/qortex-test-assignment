from django.core.exceptions import ValidationError
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.name)


class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT, related_name="albums")
    release_year = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.id} {self.artist}'s album at {self.release_year}"


class Song(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.title)


class AlbumSong(models.Model):
    album = models.ForeignKey(Album, related_name="songs", on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name="album_songs", on_delete=models.CASCADE)
    order_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ["album", "song"]

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.album.songs.all().count() + 1
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.song}"
