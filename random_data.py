import random
from faker import Faker

fake = Faker()


# Функция для генерации случайных данных
def generate_random_books(count: int = 100):
    books = []
    for _ in range(count):
        book = {
            "id": None,
            "title": fake.sentence(nb_words=3),
            "author": fake.name(),
            "year": random.randint(1900, 2023),
            "status": random.choice(["в наличии", "выдана"])
        }
        books.append(book)
    return books


# Генерация и сохранение книг в библиотеку
def populate_library(library, count: int = 10):
    books = generate_random_books(count)
    for book in books:
        print(books)
        library.add_book(book["title"], book["author"], book["year"])


if __name__ == "__main__":
    from main import Library  # Импорт библиотеки из основного кода

    library = Library()
    num_books = int(input("Введите количество книг для генерации: "))
    populate_library(library, num_books)
    library.display_books()
