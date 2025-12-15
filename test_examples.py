
"""Примеры тестов с assertRaises."""

import unittest
import os

class TestAssertRaisesExamples(unittest.TestCase):
    """Примеры использования assertRaises."""

    def test_example_1_zero_division(self):
        """Пример 1: Деление на ноль."""
        def divide(a, b):
            return a / b

        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

        self.assertEqual(divide(10, 2), 5.0)
        self.assertEqual(divide(5, 2), 2.5)

    def test_example_2_value_error(self):
        """Пример 2: ValueError при преобразовании строки."""
        with self.assertRaises(ValueError):
            int("не число")

        self.assertEqual(int("123"), 123)
        self.assertEqual(int("-456"), -456)

    def test_example_3_type_error(self):
        """Пример 3: TypeError при операциях с разными типами."""
        with self.assertRaises(TypeError):
            result = "строка" + 123

        self.assertEqual("строка" + "123", "строка123")
        self.assertEqual(100 + 200, 300)

    def test_example_4_index_error(self):
        """Пример 4: IndexError при обращении к несуществующему индексу."""
        lst = [1, 2, 3, 4, 5]

        self.assertEqual(lst[0], 1)
        self.assertEqual(lst[4], 5)

        with self.assertRaises(IndexError):
            value = lst[10]

        with self.assertRaises(IndexError):
            value = lst[-10]

    def test_example_5_key_error(self):
        """Пример 5: KeyError при обращении к несуществующему ключу."""
        d = {"name": "Иван", "age": 25, "city": "Москва"}

        self.assertEqual(d["name"], "Иван")
        self.assertEqual(d["age"], 25)

        with self.assertRaises(KeyError):
            value = d["phone"]

        with self.assertRaises(KeyError):
            value = d["адрес"]

    def test_example_6_attribute_error(self):
        """Пример 6: AttributeError при обращении к несуществующему атрибуту."""
        class Person:
            def __init__(self, name):
                self.name = name

        person = Person("Алексей")

        self.assertEqual(person.name, "Алексей")

        with self.assertRaises(AttributeError):
            value = person.age

        with self.assertRaises(AttributeError):
            value = person.phone_number

    def test_example_7_file_not_found(self):
        """Пример 7: FileNotFoundError."""
        def read_file(filename):
            if not os.path.exists(filename):
                raise FileNotFoundError(f"Файл {filename} не найден")
            with open(filename, 'r') as f:
                return f.read()

        with self.assertRaises(FileNotFoundError):
            read_file("несуществующий_файл_12345.txt")

    def test_example_8_custom_exception(self):
        """Пример 8: Пользовательские исключения."""
        class NegativeNumberError(Exception):
            pass

        def process_positive_number(num):
            if num < 0:
                raise NegativeNumberError("Число должно быть положительным")
            return num * 2

        self.assertEqual(process_positive_number(5), 10)
        self.assertEqual(process_positive_number(0), 0)

        with self.assertRaises(NegativeNumberError):
            process_positive_number(-5)

        with self.assertRaises(NegativeNumberError):
            process_positive_number(-100)

    def test_multiple_assertions_in_one_test(self):
        """Несколько проверок в одном тесте."""
        def process_data(data, operation):
            if not isinstance(data, (int, float)):
                raise TypeError("Данные должны быть числом")

            if operation == "divide" and data == 0:
                raise ValueError("Нельзя делить на ноль")

            if operation == "sqrt" and data < 0:
                raise ValueError("Нельзя извлечь корень из отрицательного числа")

            return data

        self.assertEqual(process_data(10, "add"), 10)

        with self.assertRaises(TypeError):
            process_data("строка", "add")

        with self.assertRaises(ValueError):
            process_data(0, "divide")

        with self.assertRaises(ValueError):
            process_data(-5, "sqrt")

if __name__ == '__main__':
    unittest.main()
