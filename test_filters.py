
"""Тесты для модуля filters.py."""

import unittest
from booklib.models import Book
from booklib.filters import BookFilter

class TestBookFilter(unittest.TestCase):
    """Тесты для класса BookFilter."""

    def setUp(self):
        self.books = [
            Book("Война и мир", "Лев Толстой", 1869, "Роман"),
            Book("Преступление и наказание", "Фёдор Достоевский", 1866, "Роман"),
            Book("Мастер и Маргарита", "Михаил Булгаков", 1967, "Роман"),
        ]
        self.filter = BookFilter()

    def test_search_by_author(self):
        """Поиск по автору."""
        results = self.filter.search_books(self.books, author="Толстой")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Война и мир")

    def test_search_by_title(self):
        """Поиск по названию."""
        results = self.filter.search_books(self.books, title="Мастер")
        self.assertEqual(len(results), 1)

    def test_search_by_year(self):
        """Поиск по году."""
        results = self.filter.search_books(self.books, year=1869)
        self.assertEqual(len(results), 1)

    def test_search_no_results(self):
        """Поиск без результатов."""
        results = self.filter.search_books(self.books, author="Несуществующий")
        self.assertEqual(len(results), 0)

    def test_sort_by_title(self):
        """Сортировка по названию."""
        sorted_books = self.filter.sort_books(self.books, sort_by='title')
        self.assertEqual(sorted_books[0].title, "Война и мир")

    def test_sort_by_author(self):
        """Сортировка по автору."""
        sorted_books = self.filter.sort_books(self.books, sort_by='author')
        authors = [b.author for b in sorted_books]
        self.assertEqual(authors[0], "Лев Толстой")

    def test_assert_raises_in_filters(self):
        """Демонстрация assertRaises в контексте фильтров."""
        def validate_search_params(author):
            if author and not isinstance(author, str):
                raise TypeError("Автор должен быть строкой")
            return True

        self.assertTrue(validate_search_params("Толстой"))

        with self.assertRaises(TypeError):
            validate_search_params(123)

if __name__ == '__main__':
    unittest.main()
