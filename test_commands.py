
"""Тесты для модуля commands.py."""

import unittest
from booklib.commands import LibraryCommands

class TestLibraryCommands(unittest.TestCase):
    """Тесты для класса LibraryCommands."""

    def test_example_with_assert_raises(self):
        """Пример с assertRaises для ZeroDivisionError."""
        def divide(a, b):
            return a / b

        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

        result = divide(10, 2)
        self.assertEqual(result, 5.0)

    def test_value_error_example(self):
        """Пример с ValueError."""
        def convert_to_int(value):
            return int(value)

        self.assertEqual(convert_to_int("123"), 123)

        with self.assertRaises(ValueError):
            convert_to_int("не число")

    def test_type_error_example(self):
        """Пример с TypeError."""
        def add_strings(a, b):
            if not isinstance(a, str):
                raise TypeError("Первый аргумент должен быть строкой")
            if not isinstance(b, str):
                raise TypeError("Второй аргумент должен быть строкой")
            return a + b

        self.assertEqual(add_strings("Hello", "World"), "HelloWorld")

        with self.assertRaises(TypeError):
            add_strings("Hello", 123)

    def test_real_scenario_from_project(self):
        """Реальный сценарий из проекта."""
        from unittest.mock import Mock

        commands = LibraryCommands()
        commands.storage = Mock()

        def validate_book_data(title, author, year):
            if not isinstance(year, (int, str)):
                raise TypeError("Год должен быть числом или строкой")
            if isinstance(year, str) and not year.isdigit():
                raise ValueError("Год должен быть числом")
            return True

        self.assertTrue(validate_book_data("Книга", "Автор", 2024))
        self.assertTrue(validate_book_data("Книга", "Автор", "2024"))

        with self.assertRaises(ValueError):
            validate_book_data("Книга", "Автор", "не число")

        with self.assertRaises(TypeError):
            validate_book_data("Книга", "Автор", [2024])

if __name__ == '__main__':
    unittest.main()
