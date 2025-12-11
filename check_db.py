"""
Скрипт для проверки состояния базы данных.
"""


def check_database():
    print("=== Проверка состояния PostgreSQL базы данных ===")

    try:
        from booklib.db_storage import PostgreSQLStorage

        storage = PostgreSQLStorage()
        books = storage.get_all_books()

        print(f"✅ Подключение к PostgreSQL успешно")
        print(f"📚 Книг в базе: {len(books)}")

        if books:
            print("\nПоследние книги:")
            for book in books[-5:]:
                print(f"  - '{book.title}' - {book.author}")

        return True

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


if __name__ == "__main__":
    check_database()