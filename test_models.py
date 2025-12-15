
"""Тесты для класса Book из модуля models.py."""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(''))
from booklib.models import Book

class TestBook(unittest.TestCase):
    """Тестовый класс для проверки класса Book."""

    def test_book_creation(self):
        """Тест создания книги с правильными данными."""
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман")

        self.assertEqual(book.title, "Война и мир")
        self.assertEqual(book.author, "Лев Толстой")
        self.assertEqual(book.year, 1869)
        self.assertEqual(book.genre, "Роман")
        self.assertEqual(book.quotes, [])
        self.assertIsNone(book.id)

    def test_book_creation_with_quotes(self):
        """Тест создания книги с цитатами."""
        quotes = ["Цитата 1", "Цитата 2"]
        book = Book("Книга", "Автор", 2000, "Жанр", quotes=quotes)
        self.assertEqual(book.quotes, quotes)

    def test_book_creation_without_quotes(self):
        """Тест создания книги без указания цитат."""
        book = Book("Книга", "Автор", 2000, "Жанр")
        self.assertEqual(book.quotes, [])

    def test_book_creation_with_none_quotes(self):
        """Тест создания книги с None в качестве цитат."""
        book = Book("Книга", "Автор", 2000, "Жанр", quotes=None)
        self.assertEqual(book.quotes, [])

    def test_to_dict_method(self):
        """Тест метода to_dict()."""
        book = Book("Гарри Поттер", "Джоан Роулинг", 1997, "Фэнтези", ["Магия!"])

        expected = {
            'title': 'Гарри Поттер',
            'author': 'Джоан Роулинг',
            'year': 1997,
            'genre': 'Фэнтези',
            'quotes': ['Магия!']
        }
        self.assertEqual(book.to_dict(), expected)

    def test_str_method(self):
        """Тест строкового представления книги."""
        book = Book("Мастер и Маргарита", "Михаил Булгаков", 1967, "Роман")
        expected = "'Мастер и Маргарита' - Михаил Булгаков (1967)"
        self.assertEqual(str(book), expected)

    def test_book_id_can_be_set(self):
        """Тест установки id книги."""
        book = Book("Книга", "Автор", 2000, "Жанр")
        self.assertIsNone(book.id)
        book.id = 5
        self.assertEqual(book.id, 5)

if __name__ == '__main__':
    unittest.main()
