from typing import Dict, Union

from status import Status


class Book:
    """
    Класс для представления книги.

    Атрибуты:
    ----------
    id : str
        Уникальный идентификатор книги.
    title : str
        Название книги.
    author : str
        Автор книги.
    year : int
        Год издания книги.
    status : Status
        Статус доступности книги (по умолчанию Status.AVAILABLE).

    Методы:
    -------
    to_dict() -> Dict:
        Преобразует объект Book в словарь.
    from_dict(data: Dict[str, Union[int, str]]) -> 'Book':
        Создает объект Book из словаря.
    """

    def __init__(self, id: str, title: str, author: str, year: int, status: Status = Status.AVAILABLE):
        """
        Создает все необходимые атрибуты для объекта Book.

        Параметры:
        ----------
        id : str
            Уникальный идентификатор книги.
        title : str
            Название книги.
        author : str
            Автор книги.
        year : int
            Год издания книги.
        status : Status, optional
            Статус доступности книги (по умолчанию Status.AVAILABLE).
        """
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict:
        """
        Преобразует объект Book в словарь.

        Возвращает:
        -------
        Dict
            Словарь, представляющий объект Book.
        """
        return {
            "id": str(self.id),
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status.value
        }

    @staticmethod
    def from_dict(data: Dict[str, Union[int, str]]) -> 'Book':
        """
        Создает объект Book из словаря.

        Параметры:
        ----------
        data : Dict[str, Union[int, str]]
            Словарь, содержащий атрибуты книги.

        Возвращает:
        -------
        Book
            Объект Book, созданный из словаря.
        """
        return Book(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=Status(data["status"])
        )
