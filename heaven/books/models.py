from django_extensions.db.models import TimeStampedModel
from django.db.models import CharField
from django.db.models import TextField


class Book(TimeStampedModel):
    external_id = CharField(max_length=255)
    content = TextField()
    metadata = TextField()
