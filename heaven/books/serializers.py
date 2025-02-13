from rest_framework.serializers import ModelSerializer

from books.models import Book


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "external_id", "content", "metadata", "created", "modified")


class LastViewedSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "external_id", "metadata")
