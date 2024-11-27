import datetime
import json
import logging
from typing import List, Dict
from logger import configure_logging

log = logging.getLogger(__name__)
configure_logging(level=logging.INFO)

class Book:
    """
    Класс, представляющий книгу.
    """

    def __init__(self, title: str, author: str, year: int):
        self.id = None
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"
        self.created_at = str(datetime.datetime.now().strftime('%Y-%B-%d %H:%M'))
        self.deleted_at = None

    def to_dict(self) -> Dict:
        """
        Возвращает данные книги в виде словаря.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
            "created_at": self.created_at,
            "deleted_at": self.deleted_at
        }

    def display_book(self):
        """
        Отображение книги
        """
        return (f"ID: {self.id}, Название: {self.title}, Автор: {self.author}, "
                f"Год: {self.year}, Статус: {self.status}, Дата создания: {self.created_at}")

    @staticmethod
    def from_dict(data: Dict):
        """
        Создает объект Book из словаря.
        """
        book = Book(data["title"], data["author"], data["year"])
        book.id = data["id"]
        book.status = data["status"]
        return book


class Library:
    """
    Класс, представляющий библиотеку.
    """

    def __init__(self, storage_file: str = "library.json", storage_deleted_books: str = 'deleted_books.json'):
        self.storage_file = storage_file
        self.storage_deleted_books = storage_deleted_books
        self.books: List[Book] = []
        self.deleted_books: List[Book] = []
        self.load_books()

    def load_books(self):
        """
        Загружает книги из файла.
        """
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def save_books(self):
        """
        Сохраняет все книги в файл.
        """
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def save_deleted_books(self):
        """
        Сохраняет удаленные книги в файл.
        """
        with open(self.storage_deleted_books, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.deleted_books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """
        Добавляет новую книгу в библиотеку.
        """
        new_book = Book(title, author, year)
        new_book.id = self.books[-1:][0].id + 1 if self.books else 1 # Генерация уникального ID
        self.books.append(new_book)
        self.save_books()
        log.info(f"Книга '{title}' успешно добавлена.")

    def remove_book(self, book_id: int):
        """
        Удаляет книгу по ID.
        В library.json книга помечается как удаленная и отдельно deleted_books.json будут храниться все те книги которые удалили
        """
        book = self.find_book_by_id(book_id)
        if book:
            book.deleted_at = str(datetime.datetime.now().strftime('%Y-%B-%d %H:%M'))
            self.deleted_books.append(book)
            self.save_books()
            self.save_deleted_books()
            log.info(f"Книга с ID {book_id} удалена.")
        else:
            log.info(f"Книга с ID {book_id} не найдена.")

    def search_books(self, **kwargs):
        """
        Ищет книги по заданным критериям.
        """
        results = self.books
        for key, value in kwargs.items():
            results = [book for book in results if getattr(book, key, None) == value]
        return results

    def display_books(self):
        """
        Отображает все книги в библиотеке.
        """
        if not self.books:
            log.info("Библиотека пуста.")
            return
        for book in self.books:
            if not book.deleted_at:
                log.info(book.display_book())

    def change_status(self, book_id: int, new_status: str):
        """
        Изменяет статус книги.
        """
        book = self.find_book_by_id(book_id)
        if book:
            if new_status in ["в наличии", "выдана"]:
                book.status = new_status
                self.save_books()
                log.info(f"Статус книги с ID {book_id} изменен на '{new_status}'.")
            else:
                log.info("Некорректный статус. Допустимые значения: 'в наличии', 'выдана'.")
        else:
            log.info(f"Книга с ID {book_id} не найдена.")

    def find_book_by_id(self, book_id: int) -> Book | None:
        """
        Находит книгу по ID.
        """
        try:
            book = self.books[book_id - 1]
            if not book.deleted_at:
                return book
            return None
        except IndexError:
            return None


def main():
    """
    Главная функция приложения.
    """
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")
        try:
            choice = input("Выберите действие: ")

            if choice == "1":
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания книги: "))
                library.add_book(title, author, year)
            elif choice == "2":
                try:
                    book_id = int(input("Введите ID книги для удаления: "))
                    library.remove_book(book_id)
                except ValueError:
                    log.info('Некорректный ввод данных')
            elif choice == "3":
                search_field = input("Искать по (title/author/year): ")
                search_value = input("Введите значение для поиска: ")
                if search_field == "year":
                    search_value = int(search_value)
                results = library.search_books(**{search_field: search_value})
                if results:
                    for book in results:
                        log.info(book.display_book())
                else:
                    log.info("Книги не найдены.")
            elif choice == "4":
                library.display_books()
            elif choice == "5":
                try:
                    book_id = int(input("Введите ID книги: "))
                    new_status = input("Введите новый статус (в наличии/выдана): ")
                    library.change_status(book_id, new_status)
                except ValueError:
                    log.info('Некорректный ввод данных')
            elif choice == "6":
                log.info("Выход из программы.")
                break
            else:
                log.info("Некорректный выбор. Попробуйте снова.")

        except KeyboardInterrupt:
            log.info('Пока!')
            break


if __name__ == "__main__":
    main()
