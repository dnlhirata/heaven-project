from analyzers.clients.groq import GroqClient
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.viewsets import ModelViewSet

from books.clients.gutenberg import GutenbergClient
from books.models import Book
from books.serializers import BookSerializer, LastViewedSerializer
from books.utils import get_random_chunk


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "external_id"

    def create(self, request, *args, **kwargs):
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            book_id = self.kwargs.get(self.lookup_field)
            content = GutenbergClient().get_book_content(book_id=book_id)
            metadata = GutenbergClient().get_book_metadata(book_id=book_id)
            instance = Book.objects.create(
                external_id=book_id, content=content, metadata=metadata
            )

        instance.viewed_by.add(request.user)
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data)

    @action(detail=True)
    def generate_questions(self, request, external_id=None):
        instance = self.get_object()
        groq_client = GroqClient()
        chunk = get_random_chunk(
            content=instance.content, chunk_size=20000, token_limit=25000
        )
        result, status_code = groq_client.generate_questions(chunk=chunk)

        return Response({"chunk": chunk, "questions": result}, status=status_code)

    @action(detail=False, serializer_class=LastViewedSerializer)
    def last_viewed(self, request):
        books = request.user.viewed_books.all()
        serializer = self.get_serializer(instance=books, many=True)
        return Response(serializer.data)
