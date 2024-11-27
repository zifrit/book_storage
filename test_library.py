import unittest
import os
from main import Library

class TestLibrary(unittest.TestCase):
    def setUp(self):
        """
        Подготовка тестовой библиотеки перед каждым тестом.
        """
        self.test_file = "test_library.json"
        self.test_deleted_file = "test_deleted_books.json"
        self.library = Library(storage_file=self.test_file, storage_deleted_books=self.test_deleted_file)

    def tearDown(self):
        """
        Удаление временных файлов после каждого теста.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_deleted_file):
            os.remove(self.test_deleted_file)

    def test_add_book(self):
        """
        Тест добавления книги.
        """
        self.library.add_book("Тестовая книга", "Автор Тест", 2024)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Тестовая книга")

    def test_remove_book(self):
        """
        Тест удаления книги.
        """
        self.library.add_book("Удаляемая книга", "Автор Удаления", 2023)
        book_id = self.library.books[0].id
        self.library.remove_book(book_id)
        self.assertEqual(len(self.library.deleted_books), 1)
        self.assertIsNotNone(self.library.books[0].deleted_at)

    def test_search_books(self):
        """
        Тест поиска книг.
        """
        self.library.add_book("Книга 1", "Автор 1", 2020)
        self.library.add_book("Книга 2", "Автор 2", 2021)
        results = self.library.search_books(author="Автор 1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Автор 1")

    def test_change_status(self):
        """
        Тест изменения статуса книги.
        """
        self.library.add_book("Книга для статуса", "Автор статуса", 2022)
        book_id = self.library.books[0].id
        self.library.change_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_file_creation(self):
        """
        Тест создания файла, если его нет.
        """
        self.assertFalse(os.path.exists(self.test_file))
        self.library.save_books()
        self.assertTrue(os.path.exists(self.test_file))

    def test_invalid_remove(self):
        """
        Тест удаления несуществующей книги.
        """
        self.library.remove_book(999)
        self.assertEqual(len(self.library.deleted_books), 0)

if __name__ == "__main__":
    unittest.main()
