import requests


class GutenbergClient:
    def __init__(self):
        self.base_url = 'https://www.gutenberg.org'
    
    def get_book_content(self, book_id: int):
        url = f'{self.base_url}/files/{book_id}/{book_id}-0.txt'
        response = requests.get(url)
        return response.text
    
    def get_book_metadata(self, book_id: int):
        url = f'{self.base_url}/ebooks/{book_id}'
        response = requests.get(url)
        return response