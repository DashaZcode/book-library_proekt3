"""
Модуль для работы с PostgreSQL.
"""

import psycopg2
from .models import Book


class PostgreSQLStorage:
    """Класс для работы с PostgreSQL."""

    def __init__(self, dbname="book_library", user="postgres", password="12345", host="localhost", port="5432"):
        """Инициализация подключения к БД."""
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self._check_and_init_tables()

    def _connect(self):
        """Создает подключение к БД."""
        return psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def _check_and_init_tables(self):
        """Проверяет и создает таблицы если их нет."""
        try:
            conn = self._connect()
            cur = conn.cursor()

            # Проверяем таблицу books
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'books'
                )
            """)
            books_table_exists = cur.fetchone()[0]

            # Проверяем таблицу quotes
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'quotes'
                )
            """)
            quotes_table_exists = cur.fetchone()[0]

            # Создаем таблицы если их нет
            if not books_table_exists:
                print("Создаю таблицу books...")
                cur.execute("""
                    CREATE TABLE books (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(200) NOT NULL,
                        author VARCHAR(100) NOT NULL,
                        year INTEGER NOT NULL,
                        genre VARCHAR(50) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

            if not quotes_table_exists:
                print("Создаю таблицу quotes...")
                cur.execute("""
                    CREATE TABLE quotes (
                        id SERIAL PRIMARY KEY,
                        book_id INTEGER NOT NULL,
                        quote TEXT NOT NULL,
                        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
                    )
                """)

            conn.commit()
            cur.close()
            conn.close()

        except psycopg2.OperationalError as e:
            if "database" in str(e) and "does not exist" in str(e):
                self._create_database()
                self._create_tables()
            else:
                raise e

    def _create_database(self):
        """Создает базу данных если она не существует."""
        print(f"Создаю базу данных '{self.dbname}'...")

        conn = psycopg2.connect(
            dbname="postgres",
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"CREATE DATABASE {self.dbname}")

        cur.close()
        conn.close()

        print(f"База данных '{self.dbname}' создана")

    def _create_tables(self):
        """Создает таблицы в базе данных."""
        print("Создаю таблицы...")

        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                author VARCHAR(100) NOT NULL,
                year INTEGER NOT NULL,
                genre VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur.execute("""
            CREATE TABLE quotes (
                id SERIAL PRIMARY KEY,
                book_id INTEGER NOT NULL,
                quote TEXT NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        cur.close()
        conn.close()

        print("Таблицы созданы")

    def get_all_books(self):
        """Получает все книги из БД."""
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("SELECT id, title, author, year, genre FROM books ORDER BY id")
        books_data = cur.fetchall()

        books = []
        for book_data in books_data:
            book_id, title, author, year, genre = book_data

            cur.execute("SELECT quote FROM quotes WHERE book_id = %s", (book_id,))
            quotes_data = cur.fetchall()
            quotes = [q[0] for q in quotes_data]

            book = Book(title, author, year, genre, quotes)
            book.id = book_id
            books.append(book)

        cur.close()
        conn.close()
        return books

    def add_book(self, book):
        """Добавляет книгу в БД."""
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO books (title, author, year, genre)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (book.title, book.author, book.year, book.genre))

        book_id = cur.fetchone()[0]
        conn.commit()

        for quote in book.quotes:
            self.add_quote_to_book(book_id, quote)

        cur.close()
        conn.close()
        return book_id

    def add_quote_to_book(self, book_id, quote):
        """Добавляет цитату к книге."""
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO quotes (book_id, quote)
            VALUES (%s, %s)
        """, (book_id, quote))

        conn.commit()
        cur.close()
        conn.close()

    def remove_book(self, book_id):
        """Удаляет книгу из БД."""
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("DELETE FROM books WHERE id = %s", (book_id,))
        conn.commit()

        cur.close()
        conn.close()

    def remove_quote(self, book_id, quote_index):
        """Удаляет цитату по индексу."""
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("SELECT id FROM quotes WHERE book_id = %s ORDER BY id", (book_id,))
        quotes = cur.fetchall()

        if 0 <= quote_index < len(quotes):
            quote_id = quotes[quote_index][0]
            cur.execute("DELETE FROM quotes WHERE id = %s", (quote_id,))
            conn.commit()
            success = True
        else:
            success = False

        cur.close()
        conn.close()
        return success

    def export_to_csv(self, filename='library_export.csv'):
        """Экспортирует данные из БД в CSV файл."""
        import csv

        books = self.get_all_books()

        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'author', 'year', 'genre', 'quotes'])

            for book in books:
                quotes_str = '|'.join(book.quotes)
                writer.writerow([book.title, book.author, book.year, book.genre, quotes_str])

        print(f"Данные экспортированы в {filename} ({len(books)} книг)")