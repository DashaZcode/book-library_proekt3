from .models import Book
from .storage import LibraryStorage
from .filters import BookFilter

class LibraryCommands:
    def __init__(self):
        # Убираем параметр storage_file
        self.storage = LibraryStorage()

    def add_book(self, title, author, year, genre):
        """Добавляет новую книгу в библиотеку."""
        try:
            year = int(year)
            book = Book(title, author, year, genre)
            self.storage.add_book(book)
            print(f"Книга '{title}' успешно добавлена в базу данных!")
        except ValueError:
            print("Ошибка: год должен быть числом")
        except Exception as e:
            print(f"Ошибка при добавлении книги: {e}")

    def remove_book(self, title=None, author=None):
        """Удаляет книгу из библиотеки."""
        books = self.storage.get_all_books()
        books_to_remove = []

        for book in books:
            title_match = title is None or title.lower() in book.title.lower()
            author_match = author is None or author.lower() in book.author.lower()

            if title_match and author_match:
                books_to_remove.append(book)

        if not books_to_remove:
            print("Книги не найдены")
            return

        if len(books_to_remove) == 1:
            book = books_to_remove[0]
            self.storage.remove_book(book.id)  # Передаем ID книги!
            print(f"Книга '{book.title}' удалена!")
        else:
            print("Найдено несколько книг:")
            for i, book in enumerate(books_to_remove, 1):
                print(f"{i}. {book}")

            try:
                choice = int(input("Выберите номер книги для удаления: ")) - 1
                if 0 <= choice < len(books_to_remove):
                    self.storage.remove_book(books_to_remove[choice].id)  # Передаем ID!
                    print("Книга удалена!")
            except (ValueError, IndexError):
                print("Неверный выбор")

    def list_books(self, sort_by='title', reverse=False):
        """Выводит список всех книг в библиотеке."""
        books = self.storage.get_all_books()
        sorted_books = BookFilter().sort_books(books, sort_by, reverse)

        if not sorted_books:
            print("Библиотека пуста")
            return

        print("\nСписок книг в библиотеке (из PostgreSQL):")
        print("-" * 60)
        print(f"Всего книг: {len(sorted_books)}")

        for i, book in enumerate(sorted_books, 1):
            quotes_count = len(book.quotes)
            print(f"{i}. '{book.title}' - {book.author} ({book.year}), {book.genre} [цитат: {quotes_count}]")

    def search_books(self, author=None, title=None, year=None, genre=None):
        """Ищет книги по указанным критериям."""
        try:
            if year:
                year = int(year)

            books = self.storage.get_all_books()
            results = BookFilter().search_books(
                books, author=author, title=title, year=year, genre=genre
            )

            if not results:
                print("Книги не найдены")
                return

            print(f"\nНайдено {len(results)} книг:")
            for i, book in enumerate(results, 1):
                print(f"{i}. {book}")
        except ValueError:
            print("Ошибка: год должен быть числом")

    def add_quote(self, title, author, quote):
        """Добавляет цитату к книге."""
        books = self.storage.get_all_books()
        filtered_books = BookFilter().search_books(books, title=title, author=author)

        if not filtered_books:
            print("Книга не найдена")
            return

        if len(filtered_books) == 1:
            book = filtered_books[0]
        else:
            print("Найдено несколько книг:")
            for i, book in enumerate(filtered_books, 1):
                print(f"{i}. {book}")

            try:
                choice = int(input("Выберите номер книги: ")) - 1
                book = filtered_books[choice]
            except (ValueError, IndexError):
                print("Неверный выбор")
                return

        self.storage.add_quote_to_book(book.id, quote)
        print(f"Цитата добавлена к книге '{book.title}'")

    # ⬇⬇⬇ ЭТОТ МЕТОД ПРОПУЩЕН! ДОБАВЬ ЕГО! ⬇⬇⬇
    def remove_quote(self, title, author, quote_index=None):
        """Удаляет цитату из книги."""
        books = self.storage.get_all_books()
        filtered_books = BookFilter().search_books(books, title=title, author=author)

        if not filtered_books:
            print("Книга не найдена")
            return

        if len(filtered_books) == 1:
            book = filtered_books[0]
        else:
            print("Найдено несколько книг:")
            for i, book in enumerate(filtered_books, 1):
                print(f"{i}. {book}")

            try:
                choice = int(input("Выберите номер книги: ")) - 1
                book = filtered_books[choice]
            except (ValueError, IndexError):
                print("Неверный выбор")
                return

        if not book.quotes:
            print("У книги нет цитат")
            return

        if quote_index is None:
            print(f"Цитаты книги '{book.title}':")
            for i, quote in enumerate(book.quotes, 1):
                print(f"{i}. {quote}")

            try:
                quote_index = int(input("Выберите номер цитаты для удаления: ")) - 1
            except ValueError:
                print("Ошибка: введите число")
                return

        if self.storage.remove_quote(book.id, quote_index):
            print("Цитата удалена!")
        else:
            print("Неверный номер цитаты")
    # ⬆⬆⬆ ЭТОТ МЕТОД ПРОПУЩЕН! ДОБАВЬ ЕГО! ⬆⬆⬆

    def show_quotes(self, title=None, author=None):
        """Показывает цитаты для указанной книги или всех книг."""
        books = self.storage.get_all_books()

        if title or author:
            filtered_books = BookFilter().search_books(books, title=title, author=author)
            books = filtered_books

        if not books:
            print("Книги не найдены")
            return

        found_quotes = False
        for book in books:
            if book.quotes:
                print(f"\nЦитаты из книги '{book.title}':")
                for i, quote in enumerate(book.quotes, 1):
                    print(f"{i}. {quote}")
                found_quotes = True

        if not found_quotes:
            print("Цитаты не найдены")

    def export_to_csv(self):
        """Экспортирует данные из БД в CSV файл."""
        self.storage.export_to_csv()

    def drop_database(self):
        """Удаляет всю базу данных."""
        confirm = input("Вы уверены? Вся база данных будет удалена! (yes/no): ")

        if confirm.lower() == 'yes':
            # Подключаемся к базе postgres чтобы удалить book_library
            import psycopg2
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="11111",
                host="localhost",
                port="5432"
            )
            conn.autocommit = True  # Важно для DROP DATABASE
            cur = conn.cursor()

            # Завершаем все соединения с базой
            cur.execute("""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = 'book_library'
                AND pid <> pg_backend_pid();
            """)

            # Удаляем базу данных
            cur.execute("DROP DATABASE IF EXISTS book_library")

            cur.close()
            conn.close()

            print("База данных 'book_library' удалена!")
        else:
            print("Удаление отменено")

    def clear_database(self):
        """Очищает все данные из таблиц."""
        confirm = input("Удалить ВСЕ книги и цитаты? (yes/no): ")

        if confirm.lower() == 'yes':
            try:
                import psycopg2
                conn = psycopg2.connect(
                    dbname="book_library",
                    user="postgres",
                    password="11111",  # твой пароль из storage.py
                    host="localhost",
                    port="5432"
                )
                cur = conn.cursor()

                # Очищаем таблицы (цитаты удалятся каскадно из-за ON DELETE CASCADE)
                cur.execute("DELETE FROM books")
                conn.commit()

                cur.close()
                conn.close()

                # Очищаем локальный кэш
                self.storage.books = []

                print("✅ Все данные удалены!")

            except Exception as e:
                print(f"Ошибка: {e}")
        else:
            print("Очистка отменена")

    def edit_book(self, title, author, new_title=None, new_author=None, new_year=None, new_genre=None):
        """Редактирует существующую книгу."""
        books = self.storage.get_all_books()
        filtered_books = BookFilter().search_books(books, title=title, author=author)

        if not filtered_books:
            print("Книга не найдена")
            return

        if len(filtered_books) > 1:
            print("Найдено несколько книг:")
            for i, book in enumerate(filtered_books, 1):
                print(f"{i}. {book}")
            try:
                choice = int(input("Выберите номер книги для редактирования: ")) - 1
                book = filtered_books[choice]
            except (ValueError, IndexError):
                print("Неверный выбор")
                return
        else:
            book = filtered_books[0]

        # Сохраняем старые значения
        old_title, old_author = book.title, book.author

        # Обновляем только если переданы новые значения
        if new_title:
            book.title = new_title
        if new_author:
            book.author = new_author
        if new_year:
            try:
                book.year = int(new_year)
            except ValueError:
                print("Ошибка: год должен быть числом")
                return
        if new_genre:
            book.genre = new_genre

        # Обновляем в БД
        try:
            import psycopg2
            conn = psycopg2.connect(
                dbname="book_library",
                user="postgres",
                password="11111",
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()

            cur.execute("""
                UPDATE books 
                SET title = %s, author = %s, year = %s, genre = %s
                WHERE title = %s AND author = %s
            """, (book.title, book.author, book.year, book.genre, old_title, old_author))

            conn.commit()
            cur.close()
            conn.close()

            print(f"✅ Книга '{old_title}' успешно обновлена!")

        except Exception as e:
            print(f"❌ Ошибка при обновлении: {e}")