from book_not_found import BookNotFound
from library import Library
from status import Status


def main():
    library = Library('data.json')

    while True:
        print("\nВыберите действие:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Введите номер действия: ")

        match choice:
            case '1':
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания книги: "))
                library.add_book(title, author, year)
                print(f"Книга добавлена: {title}")

            case '2':
                book_id = input("Введите ID книги для удаления: ")
                try:
                    library.remove_book(book_id)
                except BookNotFound:
                    print('Книга не найдена')
                else:
                    print("Книга удалена.")

            case '3':
                print("По какому полю искать?\n1. title\n2. author\n3. year")
                field = input('')
                if field not in ['1', '2', '3']:
                    print("Неверный выбор. Попробуйте еще раз.")
                    continue

                query = input("Введите поисковый запрос: ")

                match field:
                    case '1':
                        found_books = library.find_books(title=query)
                    case '2':
                        found_books = library.find_books(author=query)
                    case '3':
                        if not (query.isalnum() and len(query)) == 4:
                            print("Год должен быть четырехзначным числом.")
                            continue
                        else:
                            found_books = library.find_books(year=int(query))
                    case _:
                        print("Неверный выбор. Попробуйте еще раз.")
                        continue

                if found_books:
                    for book in found_books:
                        print(
                            f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, "
                            f"Status: {book.status.value}")
                else:
                    print("Книги не найдены.")

            case '4':
                library.display_books()

            case '5':
                book_id = input("Введите ID книги для изменения статуса: ")
                print("Введите новый статус.\n1. В наличии\n2. Отсутствует")
                new_status = input()
                match new_status:
                    case '1':
                        new_status = Status.AVAILABLE
                    case '2':
                        new_status = Status.UNAVAILABLE
                    case _:
                        print('Неверный выбор. Попробуйте еще раз.')
                        continue
                try:
                    status = Status(new_status)
                    library.update_status(book_id, status)
                    print("Статус книги изменен.")
                except BookNotFound:
                    print("Книга не найденв.")

            case '6':
                break

            case _:
                print("Неверный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    main()
