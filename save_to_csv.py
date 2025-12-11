"""
Простой скрипт для сохранения базы данных в CSV.
"""

import csv
from booklib.storage import LibraryStorage


def save_to_csv(filename='library_backup.csv'):
    print(f"Сохранение базы данных в {filename}...")

    try:
        storage = LibraryStorage()

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Заголовки
            writer.writerow(['ID', 'Название', 'Автор', 'Год', 'Жанр', 'Цитаты'])

            # Данные
            for book in storage.books:
                quotes_str = ' | '.join(book.quotes) if book.quotes else ''
                writer.writerow([book.id, book.title, book.author, book.year, book.genre, quotes_str])

        print(f" Успешно сохранено {len(storage.books)} книг")
        print(f" Файл: {filename}")

    except Exception as e:
        print(f" Ошибка: {e}")


if __name__ == "__main__":
    save_to_csv()