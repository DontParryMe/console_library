import unittest
from status import Status
from book import Book


class TestBook(unittest.TestCase):

    def setUp(self):
        """Создание объектов, которые будут использоваться в тестах"""
        self.book = Book(
            id="12345",
            title="Test Book",
            author="Test Author",
            year=2020,
            status=Status.AVAILABLE
        )

        self.book_dict = {
            "id": "12345",
            "title": "Test Book",
            "author": "Test Author",
            "year": 2020,
            "status": Status.AVAILABLE.value
        }

    def test_to_dict(self):
        """Проверка правильности преобразования объекта Book в словарь"""
        self.assertEqual(self.book.to_dict(), self.book_dict)

    def test_from_dict(self):
        """Проверка правильности создания объекта Book из словаря"""
        book_from_dict = Book.from_dict(self.book_dict)
        self.assertEqual(book_from_dict.id, self.book.id)
        self.assertEqual(book_from_dict.title, self.book.title)
        self.assertEqual(book_from_dict.author, self.book.author)
        self.assertEqual(book_from_dict.year, self.book.year)
        self.assertEqual(book_from_dict.status, self.book.status)


if __name__ == '__main__':
    unittest.main()
