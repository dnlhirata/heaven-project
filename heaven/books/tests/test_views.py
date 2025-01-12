from unittest.mock import patch

from books.models import Book
from books.tests.factories import BookFactory
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

faker = Faker()


class TestBookListView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        cls.token, _ = Token.objects.get_or_create(user=cls.user)

    def test_not_authenticated(self):
        book_id = str(faker.random_int())
        url = reverse("book-detail", kwargs={"external_id": book_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    @patch("books.views.GutenbergClient.get_book_content")
    @patch("books.views.GutenbergClient.get_book_metadata")
    def test_retrieve__non_existing_book(
        self, mock_get_book_metadata, mock_get_book_content
    ):
        mock_get_book_metadata.return_value = {"title": "Test Book"}
        mock_get_book_content.return_value = "Test content"
        self.assertEqual(Book.objects.count(), 0)

        book_id = str(faker.random_int())
        url = reverse("book-detail", kwargs={"external_id": book_id})

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 1)

        book = Book.objects.first()
        self.assertIn(self.user, book.viewed_by.all())
        mock_get_book_content.assert_called_once_with(book_id=book_id)
        mock_get_book_metadata.assert_called_once_with(book_id=book_id)

    @patch("books.views.GutenbergClient.get_book_content")
    @patch("books.views.GutenbergClient.get_book_metadata")
    def test_retrieve__existing_book(
        self, mock_get_book_metadata, mock_get_book_content
    ):
        mock_get_book_metadata.return_value = {"title": "Test Book"}
        mock_get_book_content.return_value = "Test content"
        book = BookFactory()
        self.assertEqual(Book.objects.count(), 1)

        url = reverse("book-detail", kwargs={"external_id": book.external_id})

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 1)
        self.assertIn(self.user, book.viewed_by.all())
        mock_get_book_metadata.assert_not_called()
        mock_get_book_content.assert_not_called()

    @patch("books.views.GroqClient.generate_questions")
    @patch("books.views.get_random_chunk")
    def test_generate_questions(self, mock_get_random_chunk, mock_generate_questions):
        mock_get_random_chunk.return_value = "Test chunk"
        mock_generate_questions.return_value = (["Test question"], 200)

        book = BookFactory()
        url = reverse(
            "book-generate-questions", kwargs={"external_id": book.external_id}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["chunk"], "Test chunk")
        self.assertEqual(response.data["questions"], ["Test question"])

    def test_last_viewed(self):
        book = BookFactory()
        book.viewed_by.add(self.user)
        url = reverse("book-last-viewed")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            [
                {
                    "id": book.id,
                    "external_id": book.external_id,
                    "metadata": book.metadata,
                }
            ],
        )
