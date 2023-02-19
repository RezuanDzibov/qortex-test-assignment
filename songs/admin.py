from django.contrib import admin

from . import models


@admin.register(models.Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass


class AlbumSongInline(admin.StackedInline):
    model = models.AlbumSong
    readonly_fields = ["order_number"]


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    inlines = [AlbumSongInline]


@admin.register(models.Song)
class SongAdmin(admin.ModelAdmin):
    pass

