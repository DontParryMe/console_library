import io
import unittest
import os
import uuid
from contextlib import redirect_stdout

from book import Book
from book_not_found import BookNotFound
from status import Status
from library import Library


class LibraryTestCase(unittest.TestCase):
    def setUp(self):
        """Создает временный файл данных и инициализирует объект библиотеки."""
        self.data_file = "test_data.json"
        self.library = Library(data_file=self.data_file)

    def tearDown(self):
        """Удаляет временный файл данных после тестов."""
        if os.path.exists(self.data_file):
            os.remove(self.data_file)

    def test_add_book(self):
        """Тестирование добавления книги."""
        self.library.add_book("Test Book", "Test Author", 2024)
        books = self.library.find_books(title="Test Book")
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Test Book")

    def test_remove_book(self):
        """Тестирование удаления книги."""
        book_id = str(uuid.uuid4())
        self.library.books.append(Book(book_id, "Test Book", "Test Author", 2024))
        self.library.save_books()
        self.library.remove_book(book_id)
        books = self.library.find_books(title="Test Book")
        self.assertEqual(len(books), 0)

    def test_remove_nonexistent_book(self):
        """Тестирование удаления несуществующей книги."""
        with self.assertRaises(BookNotFound):
            self.library.remove_book(str(uuid.uuid4()))

    def test_find_books(self):
        """Тестирование поиска книг."""
        book_id = str(uuid.uuid4())
        self.library.books.append(Book(book_id, "Test Book", "Test Author", 2024))
        self.library.save_books()
        found_books = self.library.find_books(title="Test Book")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].title, "Test Book")
        found_books = self.library.find_books(author="Test Author")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].author, "Test Author")
        found_books = self.library.find_books(year=2024)
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].year, 2024)

    def test_update_status(self):
        """Тестирование обновления статуса книги."""
        book_id = str(uuid.uuid4())
        self.library.books.append(Book(book_id, "Test Book", "Test Author", 2024, Status.AVAILABLE))
        self.library.save_books()
        self.library.update_status(book_id, Status.UNAVAILABLE)
        books = self.library.find_books(title="Test Book")
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].status, Status.UNAVAILABLE)

    def test_update_status_nonexistent_book(self):
        """Тестирование обновления статуса несуществующей книги."""
        with self.assertRaises(BookNotFound):
            self.library.update_status(str(uuid.uuid4()), Status.UNAVAILABLE)

    def test_display_books(self):
        """Тестирование отображения книг (с перенаправлением вывода)."""
        book_id = str(uuid.uuid4())
        self.library.books.append(Book(book_id, "Test Book", "Test Author", 2024))
        self.library.save_books()
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            self.library.display_books()
        output = captured_output.getvalue().strip()
        self.assertIn("ID: " + book_id, output)
        self.assertIn("Название: Test Book", output)
        self.assertIn("Автор: Test Author", output)
        self.assertIn("Год: 2024", output)
