from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.name)


class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT, related_name="albums")
    release_year = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.artist} {self.release_year}"


class Song(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.title)


class AlbumSong(models.Model):
    album = models.ForeignKey(Album, related_name="songs", on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    order_number = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.song}"
