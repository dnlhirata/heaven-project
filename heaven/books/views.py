from django.http import Http404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from books.clients.gutenberg import GutenbergClient
from books.models import Book
from books.serializers import BookSerializer



class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    lookup_field = 'external_id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            book_id = self.kwargs.get(self.lookup_field)
            content = GutenbergClient().get_book_content(book_id=book_id)
            # metadata = GutenbergClient().get_book_metadata(book_id=book_id)
            instance = Book.objects.create(external_id=book_id, content=content, metadata=metadata)
        
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data)
