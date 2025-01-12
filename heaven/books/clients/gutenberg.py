import requests

from books.utils import parse_rdf_metadata


class GutenbergClient:
    def __init__(self):
        self.base_url = "https://www.gutenberg.org"

    def get_book_content(self, book_id: int):
        url = f"{self.base_url}/cache/epub/{book_id}/pg{book_id}.txt"
        response = requests.get(url)
        response.raise_for_status()

        return response.text

    def get_book_metadata(self, book_id: int):
        url = f"{self.base_url}/cache/epub/{book_id}/pg{book_id}.rdf"
        response = requests.get(url)
        response.raise_for_status()

        metadata = parse_rdf_metadata(response.text)
        return metadata
