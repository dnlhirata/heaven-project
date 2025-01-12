from books.models import Book
from factory import LazyAttribute
from factory.django import DjangoModelFactory
from faker import Faker

faker = Faker()


class BookFactory(DjangoModelFactory):
    external_id = LazyAttribute(lambda _: str(faker.random_int()))
    content = faker.paragraphs()

    class Meta:
        model = Book
