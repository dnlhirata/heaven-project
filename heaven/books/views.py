from django.http import Http404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from analyzers.clients.groq import GroqClient
from books.clients.gutenberg import GutenbergClient
from books.models import Book
from books.serializers import BookSerializer
from books.utils import split_content


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
            instance = Book.objects.create(external_id=book_id, content=content)
        
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data)
    
    @action(detail=True)
    def summary(self, request, external_id=None):
        instance = self.get_object()
        groq_client = GroqClient()
        text_chunks = split_content(content=instance.content)
        groq_client.initiate_summary(number_of_chunks=len(text_chunks))
        for i, chunk in enumerate(text_chunks):
            groq_client.send_content_chunk(chunk_number=i, chunk_content=chunk)
        summary = groq_client.summarize_content()
        return Response({'summary': summary})
