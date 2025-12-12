"""Скрипт для инициализации базы данных.

Запускается только 1 раз.
"""

try:
    from booklib import LibraryStorage
    storage = LibraryStorage()
    print(f"База данных успешно подключена.")
    print(f"Загружено книг: {len(storage.books)}")

except Exception as e:
    print(f" Ошибка: {e}")