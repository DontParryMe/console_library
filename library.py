import json
import os
import uuid
from typing import List, Optional
from book import Book
from book_not_found import BookNotFound
from status import Status


class Library:
    """
    Класс для управления коллекцией объектов Book.

    Атрибуты:
        data_file (str): Путь к JSON-файлу, где хранятся данные о книгах.
        books (List[Book]): Список книг в библиотеке.

    Методы:
        load_books() -> List[Book]: Загружает книги из JSON-файла.
        save_books(): Сохраняет текущий список книг в JSON-файл.
        add_book(title: str, author: str, year: int): Добавляет новую книгу в библиотеку.
        remove_book(book_id: str): Удаляет книгу из библиотеки по ID.
        find_books(title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None) -> List[Book]:
            Находит книги по названию, автору или году.
        display_books(): Выводит информацию обо всех книгах в библиотеке.
        update_status(book_id: str, status: Status): Обновляет статус книги по ID.
    """

    def __init__(self, data_file: str = "data.json"):
        """
        Инициализирует библиотеку с указанием файла данных.

        Args:
            data_file (str): Путь к JSON-файлу с данными о книгах. По умолчанию 'data.json'.
        """
        self.data_file = data_file
        self.books = self.load_books()

    def load_books(self) -> List[Book]:
        """
        Загружает книги из JSON-файла.

        Returns:
            List[Book]: Список книг, загруженных из файла.
        """
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Book.from_dict(book) for book in data]
        return []

    def save_books(self):
        """
        Сохраняет текущий список книг в JSON-файл.
        """
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """
        Добавляет новую книгу в библиотеку.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
        """
        new_book = Book(str(uuid.uuid4()), title, author, year)
        self.books.append(new_book)
        self.save_books()

    def remove_book(self, book_id: str):
        """
        Удаляет книгу из библиотеки по ID.

        Args:
            book_id (str): ID книги для удаления.

        Raises:
            BookNotFound: Если книга с указанным ID не найдена.
        """
        if next(filter(lambda item: item.id == book_id, self.books), None):
            self.books = [book for book in self.books if book.id != book_id]
            self.save_books()
        else:
            raise BookNotFound

    def find_books(self,
                   title: Optional[str] = None,
                   author: Optional[str] = None,
                   year: Optional[int] = None) -> List[Book]:
        """
        Находит книги по названию, автору или году.

        Args:
            title (Optional[str]): Название книги. По умолчанию None.
            author (Optional[str]): Автор книги. По умолчанию None.
            year (Optional[int]): Год издания книги. По умолчанию None.

        Returns:
            List[Book]: Список книг, соответствующих критериям поиска.
        """
        result = self.books
        if title:
            result = [book for book in result if title.lower() in book.title.lower()]
        if author:
            result = [book for book in result if author.lower() in book.author.lower()]
        if year:
            result = [book for book in result if book.year == year]
        return result

    def display_books(self):
        """
        Выводит информацию обо всех книгах в библиотеке.
        """
        for book in self.books:
            print(
                f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, "
                f"Статус: {book.status.value}")

    def update_status(self, book_id: str, status: Status):
        """
        Обновляет статус книги по ID.

        Args:
            book_id (str): ID книги для обновления.
            status (Status): Новый статус книги.

        Raises:
            BookNotFound: Если книга с указанным ID не найдена.
        """
        book = next(filter(lambda item: item.id == book_id, self.books), None)
        if book is not None:
            book.status = status
            self.save_books()
            return
        raise BookNotFound()
