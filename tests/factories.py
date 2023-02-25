import factory
from faker import Faker

from songs import models

fake = Faker()


class ArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Artist

    name = factory.LazyAttribute(lambda obj: fake.name())


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Album

    release_year = factory.LazyAttribute(lambda obj: fake.year())

