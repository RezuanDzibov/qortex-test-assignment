import factory
from faker import Faker

from songs import models

fake = Faker()


class ArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Artist

    name = factory.LazyAttribute(lambda obj: fake.name())
