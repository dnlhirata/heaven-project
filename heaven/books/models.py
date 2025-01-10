from django.conf import settings
from django.db.models import CharField, JSONField, ManyToManyField, TextField
from django_extensions.db.models import TimeStampedModel


class Book(TimeStampedModel):
    external_id = CharField(max_length=255)
    content = TextField()
    metadata = JSONField(default=dict)
    viewed_by = ManyToManyField(settings.AUTH_USER_MODEL, related_name="viewed_books")
